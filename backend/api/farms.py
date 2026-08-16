from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import uuid, json
from datetime import datetime, date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape

from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError, GeoPolygon, PolygonValidationResult
from services.polygon_validator import validate_farm_boundary
from services.ai_client import get_ai_client
from db.session import get_db
from db.models import Farm, User

router = APIRouter()


def _serialize_farm(f: Farm) -> dict:
    """Serialize a Farm ORM object to a full dict matching openapi.yaml Farm schema."""
    boundary = None
    centroid = {"lat": 20.5937, "lon": 78.9629}  # India geographic center as fallback

    if f.boundary is not None:
        try:
            shape = to_shape(f.boundary)
            # Convert Shapely geometry to GeoJSON-style dict
            coords = [[[lon, lat] for lon, lat in shape.exterior.coords]]
            boundary = {"type": "Polygon", "coordinates": coords}
            # Compute centroid from exterior coordinates
            lons = [c[0] for c in shape.exterior.coords]
            lats = [c[1] for c in shape.exterior.coords]
            centroid = {
                "lat": round(sum(lats) / len(lats), 6),
                "lon": round(sum(lons) / len(lons), 6),
            }
        except Exception:
            pass

    return {
        "id": str(f.id),
        "user_id": str(f.user_id),
        "name": f.name,
        "crop": f.crop,
        "sowing_date": f.sowing_date.date().isoformat() if f.sowing_date else None,
        "area_m2": f.area_m2,
        "boundary": boundary,
        "centroid": centroid,
        "status": f.status.value if f.status else "PENDING",
    }


class CreateFarmRequest(BaseModel):
    name: str
    crop: Optional[str] = None
    sowing_date: Optional[date] = None
    boundary: GeoPolygon


@router.get("", response_model=Envelope)
async def list_farms(page: int = 1, page_size: int = 50, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Farm).order_by(Farm.name, Farm.id).limit(page_size).offset(offset)
    )
    farms = result.scalars().all()
    return Envelope(
        success=True,
        data=[_serialize_farm(f) for f in farms],
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None,
    )


@router.post("", response_model=Envelope, status_code=201)
async def create_farm(req: CreateFarmRequest, db: AsyncSession = Depends(get_db)):
    val_res = validate_farm_boundary(req.boundary)
    if not val_res.valid:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(
                code="FARM_BOUNDARY_INVALID",
                message=f"Invalid boundary: {val_res.reason}",
                details={"area": val_res.area_m2},
            ),
        )

    user_result = await db.execute(select(User).limit(1))
    user = user_result.scalar_one_or_none()
    if not user:
        user = User(name="Default Farmer", language="en", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)

    coordinates = req.boundary.coordinates[0]
    points = ", ".join([f"{lon} {lat}" for lon, lat in coordinates])
    wkt_polygon = f"POLYGON(({points}))"

    new_farm = Farm(
        user_id=user.id,
        name=req.name,
        crop=req.crop,
        sowing_date=datetime.combine(req.sowing_date, datetime.min.time()) if req.sowing_date else None,
        area_m2=val_res.area_m2,
        boundary=WKTElement(wkt_polygon, srid=4326),
    )
    db.add(new_farm)
    await db.commit()
    await db.refresh(new_farm)

    return Envelope(
        success=True,
        data={"farm_id": str(new_farm.id), "area_m2": val_res.area_m2},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None,
    )


@router.get("/{farm_id}", response_model=Envelope)
async def get_farm(farm_id: str, db: AsyncSession = Depends(get_db)):
    try:
        farm_uuid = uuid.UUID(farm_id)
    except ValueError:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID"),
        )

    farm = await db.get(Farm, farm_uuid)
    if not farm:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="FARM_NOT_FOUND", message="Farm not found"),
        )

    return Envelope(
        success=True,
        data=_serialize_farm(farm),
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None,
    )


class BoundaryCheckRequest(BaseModel):
    boundary: GeoPolygon


@router.post("/{farm_id}/validate-boundary", response_model=PolygonValidationResult)
async def check_boundary(farm_id: str, req: BoundaryCheckRequest):
    return validate_farm_boundary(req.boundary)


# ─── AI PROXY ROUTES ────────────────────────────────────────────────────────

@router.post("/{farm_id}/crop-health", response_model=Envelope)
async def farm_crop_health(
    farm_id: str,
    image: UploadFile = File(...),
    crop: str = Form(...),
    growth_stage: str = Form(default="vegetative"),
    db: AsyncSession = Depends(get_db),
):
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    try:
        image_bytes = await image.read()
        ai = get_ai_client()
        result = await ai.get_crop_health(image_bytes, crop, growth_stage)
        return Envelope(success=True, data=result,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)
    except Exception as e:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message=str(e)))


@router.post("/{farm_id}/yield-predict", response_model=Envelope)
async def farm_yield_predict(farm_id: str, db: AsyncSession = Depends(get_db)):
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    try:
        area_ha = (farm.area_m2 or 10000) / 10000.0
        crop = farm.crop or "wheat"
        
        boundary_coords = None
        centroid_lat = None
        centroid_lon = None
        try:
            if farm.boundary is not None:
                shape = to_shape(farm.boundary)
                centroid_lat = shape.centroid.y
                centroid_lon = shape.centroid.x
                boundary_coords = [[lon, lat] for lon, lat in shape.exterior.coords]
        except Exception:
            pass

        ai = get_ai_client()
        result = await ai.get_yield_prediction(
            crop=crop, area_ha=area_ha,
            weather={"rainfall": 80, "temp_mean": 27, "humidity": 65},
            soil={"pH": 6.5, "N": 50, "P": 25, "K": 200, "organic_carbon": 0.5},
            satellite={"ndvi_mean": 0.5, "ndwi_mean": 0.0, "ndmi_mean": 0.0},
            boundary_coordinates=boundary_coords,
            centroid_lat=centroid_lat,
            centroid_lon=centroid_lon,
        )
        return Envelope(success=True, data=result,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)
    except Exception as e:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message=str(e)))


@router.post("/{farm_id}/risk-score", response_model=Envelope)
async def farm_risk_score(farm_id: str, db: AsyncSession = Depends(get_db)):
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    try:
        area_ha = (farm.area_m2 or 10000) / 10000.0
        crop = farm.crop or "wheat"

        boundary_coords = None
        centroid_lat = None
        centroid_lon = None
        try:
            if farm.boundary is not None:
                shape = to_shape(farm.boundary)
                centroid_lat = shape.centroid.y
                centroid_lon = shape.centroid.x
                boundary_coords = [[lon, lat] for lon, lat in shape.exterior.coords]
        except Exception:
            pass

        ai = get_ai_client()
        result = await ai.get_risk_score(
            crop=crop, area_ha=area_ha,
            weather={"rainfall": 80, "temp_mean": 28, "humidity": 65},
            soil={"pH": 6.5, "N": 50, "P": 25, "K": 200},
            satellite={"ndvi_mean": 0.5, "ndwi_mean": 0.0, "ndmi_mean": 0.0},
            history={"yield_prediction": 3000, "disease_probability": 0.1, "historical_loss": 0.1},
            boundary_coordinates=boundary_coords,
            centroid_lat=centroid_lat,
            centroid_lon=centroid_lon,
        )
        return Envelope(success=True, data=result,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)
    except Exception as e:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message=str(e)))


@router.post("/{farm_id}/advisory", response_model=Envelope)
async def farm_advisory(farm_id: str, db: AsyncSession = Depends(get_db)):
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    try:
        ai = get_ai_client()
        result = await ai.get_advisory({
            "crop": farm.crop,
            "area_ha": (farm.area_m2 or 10000) / 10000.0,
            "weather": {"temp_mean": 28, "rainfall": 80},
            "soil": {"N": 50, "P": 25, "K": 200, "pH": 6.5},
        })
        return Envelope(success=True, data=result,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)
    except Exception as e:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message=str(e)))


@router.post("/{farm_id}/soil/analyze", response_model=Envelope)
async def farm_soil_analyze(
    farm_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    try:
        file_bytes = await file.read()
        ai = get_ai_client()
        result = await ai.get_soil_ocr(file_bytes, file.filename or "soil_report")
        return Envelope(success=True, data=result,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)
    except Exception as e:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message=str(e)))


@router.get("/{farm_id}/weather/current", response_model=Envelope)
async def farm_weather_current(farm_id: str, db: AsyncSession = Depends(get_db)):
    from services.weather_client import get_current_weather
    farm = await _get_farm_or_404(farm_id, db)
    if isinstance(farm, Envelope):
        return farm
    # Use centroid from boundary if available, else India default
    lat, lon = 20.5937, 78.9629
    try:
        shape = to_shape(farm.boundary)
        c = shape.centroid
        lat, lon = c.y, c.x
    except Exception:
        pass
    weather = await get_current_weather(lat, lon)
    if not weather:
        return Envelope(success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AI_UNAVAILABLE", message="Weather service unavailable"))
    return Envelope(success=True, data=weather,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()), error=None)


# ─── Helper ──────────────────────────────────────────────────────────────────

async def _get_farm_or_404(farm_id: str, db: AsyncSession):
    """Return Farm ORM object or an error Envelope."""
    try:
        farm_uuid = uuid.UUID(farm_id)
    except ValueError:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID"),
        )
    farm = await db.get(Farm, farm_uuid)
    if not farm:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="FARM_NOT_FOUND", message="Farm not found"),
        )
    return farm

    offset = (page - 1) * page_size
    result = await db.execute(select(Farm).order_by(Farm.name, Farm.id).limit(page_size).offset(offset))
    farms = result.scalars().all()
    
    farms_list = []
    for f in farms:
        farms_list.append({
            "id": str(f.id),
            "user_id": str(f.user_id),
            "name": f.name,
            "crop": f.crop,
            "area_m2": f.area_m2,
            "status": f.status.value if f.status else "VERIFIED"
        })
        
    return Envelope(
        success=True,
        data=farms_list,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("", response_model=Envelope, status_code=201)
async def create_farm(req: CreateFarmRequest, db: AsyncSession = Depends(get_db)):
    # Validate boundary
    val_res = validate_farm_boundary(req.boundary)
    if not val_res.valid:
        return Envelope(
            success=False,
            data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(
                code="FARM_BOUNDARY_INVALID",
                message=f"Invalid boundary: {val_res.reason}",
                details={"area": val_res.area_m2}
            )
        )
        
    # Find our dummy user to act as the owner
    user_result = await db.execute(select(User).limit(1))
    user = user_result.scalar_one_or_none()
    
    if not user:
        # Create one dynamically if the DB is completely empty and they didn't hit /register
        user = User(name="Default Farmer", language="en", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    # Convert boundary to WKT
    coordinates = req.boundary.coordinates[0]
    points = ", ".join([f"{lon} {lat}" for lon, lat in coordinates])
    wkt_polygon = f"POLYGON(({points}))"
    
    new_farm = Farm(
        user_id=user.id,
        name=req.name,
        crop=req.crop,
        sowing_date=datetime.combine(req.sowing_date, datetime.min.time()) if req.sowing_date else None,
        area_m2=val_res.area_m2,
        boundary=WKTElement(wkt_polygon, srid=4326)
    )
    
    db.add(new_farm)
    await db.commit()
    await db.refresh(new_farm)
        
    return Envelope(
        success=True,
        data={"farm_id": str(new_farm.id), "area_m2": val_res.area_m2},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/{farm_id}", response_model=Envelope)
async def get_farm(farm_id: str, db: AsyncSession = Depends(get_db)):
    try:
        farm_uuid = uuid.UUID(farm_id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID")
        )
        
    farm = await db.get(Farm, farm_uuid)
    if not farm:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="NOT_FOUND", message="Farm not found")
        )
        
    return Envelope(
        success=True,
        data={
            "id": str(farm.id), 
            "name": farm.name,
            "crop": farm.crop,
            "area_m2": farm.area_m2,
            "status": farm.status.value if farm.status else "VERIFIED"
        },
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

class BoundaryCheckRequest(BaseModel):
    boundary: GeoPolygon

@router.post("/{farm_id}/validate-boundary", response_model=PolygonValidationResult)
async def check_boundary(farm_id: str, req: BoundaryCheckRequest):
    return validate_farm_boundary(req.boundary)
