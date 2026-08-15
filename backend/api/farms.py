from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime, date
from typing import Optional
from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError, GeoPolygon, PolygonValidationResult
from services.polygon_validator import validate_farm_boundary

router = APIRouter()

class CreateFarmRequest(BaseModel):
    name: str
    crop: Optional[str] = None
    sowing_date: Optional[date] = None
    boundary: GeoPolygon

@router.get("", response_model=Envelope)
async def list_farms(page: int = 1, page_size: int = 20):
    return Envelope(
        success=True,
        data=[], # Empty list for now
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("", response_model=Envelope, status_code=201)
async def create_farm(req: CreateFarmRequest):
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
        
    return Envelope(
        success=True,
        data={"farm_id": str(uuid.uuid4()), "area_m2": val_res.area_m2},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/{farm_id}", response_model=Envelope)
async def get_farm(farm_id: str):
    return Envelope(
        success=True,
        data={"id": farm_id, "name": "Mock Farm"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

class BoundaryCheckRequest(BaseModel):
    boundary: GeoPolygon

@router.post("/{farm_id}/validate-boundary", response_model=PolygonValidationResult)
async def check_boundary(farm_id: str, req: BoundaryCheckRequest):
    return validate_farm_boundary(req.boundary)
