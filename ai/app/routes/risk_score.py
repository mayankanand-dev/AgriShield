"""Risk scoring endpoint."""
from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/")
async def calculate_risk(
    weather: dict = Body(...),
    crop: str = Body(...),
    soil: dict = Body(...),
    history: dict = Body(None)
):
    """Calculate farm risk score."""
    # TODO: Implement risk scoring
    return {
        "risk_score": 0.45,
        "risk_band": "low",
        "factors": []
    }
