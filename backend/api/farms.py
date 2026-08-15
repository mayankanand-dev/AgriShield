from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement

from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError, GeoPolygon, PolygonValidationResult
from services.polygon_validator import validate_farm_boundary
from db.session import get_db
from db.models import Farm, User

router = APIRouter()

class CreateFarmRequest(BaseModel):
    name: str
    crop: Optional[str] = None
    sowing_date: Optional[date] = None
    boundary: GeoPolygon

@router.get("", response_model=Envelope)
async def list_farms(page: int = 1, page_size: int = 50, db: AsyncSession = Depends(get_db)):
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
