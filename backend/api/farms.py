from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import BaseModel
import uuid, json
from datetime import datetime, date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape

from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError, GeoPolygon, PolygonValidationResult
from services.polygon_validator import validate_farm_boundary
from services.ai_client import get_ai_client
from db.session import get_db
from db.models import Farm, User, UserRole
from api.auth import get_current_user, get_admin_user, _ok, _error

router = APIRouter()

def _serialize_farm(f: Farm, include_farmer=False) -> dict:
    """Serialize a Farm ORM object to a dict matching openapi.yaml Farm schema."""
    boundary = None
    centroid = {"lat": 20.5937, "lon": 78.9629}  # India geographic center as fallback

    if f.boundary is not None:
        try:
            shape = to_shape(f.boundary)
            coords = [[[lon, lat] for lon, lat in shape.exterior.coords]]
            boundary = {"type": "Polygon", "coordinates": coords}
            lons = [c[0] for c in shape.exterior.coords]
            lats = [c[1] for c in shape.exterior.coords]
            centroid = {
                "lat": round(sum(lats) / len(lats), 6),
                "lon": round(sum(lons) / len(lons), 6),
            }
        except Exception:
            pass

    data = {
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
    
    if include_farmer and f.owner:
        data["farmer"] = {
            "id": str(f.owner.id),
            "name": f.owner.name,
            "phone": f.owner.phone
        }
        
    return data

class CreateFarmRequest(BaseModel):
    name: str
    crop: Optional[str] = None
    sowing_date: Optional[date] = None
    boundary: GeoPolygon

@router.get("")
async def list_farms(
    page: int = 1, 
    page_size: int = 50, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    query = select(Farm).options(selectinload(Farm.owner)).order_by(Farm.name, Farm.id)
    
    if current_user.role != UserRole.ADMIN:
        query = query.where(Farm.user_id == current_user.id)
        
    query = query.limit(page_size).offset(offset)
    result = await db.execute(query)
    farms = result.scalars().all()
    
    # If admin, include farmer details
    is_admin = current_user.role == UserRole.ADMIN
    return _ok([_serialize_farm(f, include_farmer=is_admin) for f in farms])

@router.post("", status_code=201)
async def create_farm(
    req: CreateFarmRequest, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    val_res = validate_farm_boundary(req.boundary)
    if not val_res.valid:
        return _error("FARM_BOUNDARY_INVALID", f"Invalid boundary: {val_res.reason}", 400)

    coordinates = req.boundary.coordinates[0]
    points = ", ".join([f"{lon} {lat}" for lon, lat in coordinates])
    wkt_polygon = f"POLYGON(({points}))"

    new_farm = Farm(
        user_id=current_user.id,
        name=req.name,
        crop=req.crop,
        sowing_date=datetime.combine(req.sowing_date, datetime.min.time()) if req.sowing_date else None,
        area_m2=val_res.area_m2,
        boundary=WKTElement(wkt_polygon, srid=4326),
    )
    db.add(new_farm)
    await db.commit()
    await db.refresh(new_farm)

    return _ok({"farm_id": str(new_farm.id), "area_m2": val_res.area_m2})

@router.get("/{farm_id}")
async def get_farm(
    farm_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        farm_uuid = uuid.UUID(farm_id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")

    query = select(Farm).options(selectinload(Farm.owner)).where(Farm.id == farm_uuid)
    result = await db.execute(query)
    farm = result.scalar_one_or_none()
    
    if not farm:
        return _error("FARM_NOT_FOUND", "Farm not found", 404)
        
    if current_user.role != UserRole.ADMIN and farm.user_id != current_user.id:
        return _error("FORBIDDEN", "Not allowed to view this farm", 403)

    return _ok(_serialize_farm(farm, include_farmer=(current_user.role == UserRole.ADMIN)))

class BoundaryCheckRequest(BaseModel):
    boundary: GeoPolygon

@router.post("/{farm_id}/validate-boundary", response_model=PolygonValidationResult)
async def check_boundary(farm_id: str, req: BoundaryCheckRequest):
    return validate_farm_boundary(req.boundary)


# ─── AI PROXY ROUTES ────────────────────────────────────────────────────────

async def _get_farm_or_404(farm_id: str, db: AsyncSession, user: User):
    try:
        farm_uuid = uuid.UUID(farm_id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")
    
    farm = await db.get(Farm, farm_uuid)
    if not farm:
        return _error("FARM_NOT_FOUND", "Farm not found", 404)
        
    if user.role != UserRole.ADMIN and farm.user_id != user.id:
        return _error("FORBIDDEN", "Not allowed to access this farm", 403)
        
    return farm


@router.post("/{farm_id}/crop-health")
async def farm_crop_health(
    farm_id: str,
    image: UploadFile = File(...),
    crop: str = Form(...),
    growth_stage: str = Form(default="vegetative"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
        return farm
        
    try:
        image_bytes = await image.read()
        ai = get_ai_client()
        result = await ai.get_crop_health(image_bytes, crop, growth_stage)
        return _ok(result)
    except Exception as e:
        return _error("AI_UNAVAILABLE", str(e), 500)


@router.post("/{farm_id}/yield-predict")
async def farm_yield_predict(
    farm_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
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
        return _ok(result)
    except Exception as e:
        return _error("AI_UNAVAILABLE", str(e), 500)


@router.post("/{farm_id}/risk-score")
async def farm_risk_score(
    farm_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
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
        return _ok(result)
    except Exception as e:
        return _error("AI_UNAVAILABLE", str(e), 500)


@router.post("/{farm_id}/advisory")
async def farm_advisory(
    farm_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
        return farm
        
    try:
        ai = get_ai_client()
        result = await ai.get_advisory({
            "crop": farm.crop,
            "area_ha": (farm.area_m2 or 10000) / 10000.0,
            "weather": {"temp_mean": 28, "rainfall": 80},
            "soil": {"N": 50, "P": 25, "K": 200, "pH": 6.5},
        })
        return _ok(result)
    except Exception as e:
        return _error("AI_UNAVAILABLE", str(e), 500)


@router.post("/{farm_id}/soil/analyze")
async def farm_soil_analyze(
    farm_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
        return farm
        
    try:
        file_bytes = await file.read()
        ai = get_ai_client()
        result = await ai.get_soil_ocr(file_bytes, file.filename or "soil_report")
        return _ok(result)
    except Exception as e:
        return _error("AI_UNAVAILABLE", str(e), 500)


@router.get("/{farm_id}/weather/current")
async def farm_weather_current(
    farm_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    from services.weather_client import get_current_weather
    farm = await _get_farm_or_404(farm_id, db, current_user)
    if not isinstance(farm, Farm):
        return farm
        
    lat, lon = 20.5937, 78.9629
    try:
        shape = to_shape(farm.boundary)
        c = shape.centroid
        lat, lon = c.y, c.x
    except Exception:
        pass
        
    weather = await get_current_weather(lat, lon)
    if not weather:
        return _error("AI_UNAVAILABLE", "Weather service unavailable", 500)
    return _ok(weather)
