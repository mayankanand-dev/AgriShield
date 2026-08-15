"""Agricultural advisory endpoint."""
from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/")
async def get_advisory(farm_context: dict = Body(...)):
    """Get agricultural recommendations."""
    # TODO: Implement advisory generation
    return {
        "recommendations": [],
        "warnings": []
    }
