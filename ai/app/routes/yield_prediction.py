"""Yield prediction endpoint."""
from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/")
async def predict_yield(
    crop: str = Body(...),
    area_ha: float = Body(...),
    sowing_date: str = Body(...),
    history: dict = Body(None),
    weather: dict = Body(None)
):
    """Predict crop yield."""
    # TODO: Implement yield prediction
    return {
        "yield_value": 5000,
        "unit": "kg",
        "confidence": 0.82
    }
