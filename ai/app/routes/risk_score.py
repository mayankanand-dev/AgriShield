"""Risk scoring endpoint — calls trained RandomForest model."""
from fastapi import APIRouter, Body
from app import config
from inference.risk_scoring import score_risk

router = APIRouter()


@router.post("/")
async def calculate_risk(
    crop: str = Body(...),
    area_ha: float = Body(default=1.0),
    weather: dict = Body(default_factory=dict),
    soil: dict = Body(default_factory=dict),
    satellite: dict = Body(default_factory=dict),
    history: dict = Body(default_factory=dict),
):
    """Calculate farm risk score."""
    if config.MOCK_MODE:
        return {
            "risk_score": 0.35, "risk_band": "medium",
            "factors": [], "confidence": 0.88,
            "model_version": "mock-v1", "low_confidence": False, "inference_ms": 3,
        }

    features = {
        "crop": crop,
        "area_ha": area_ha,
        "rainfall": weather.get("rainfall", 80),
        "temp_mean": weather.get("temp_mean", 25),
        "humidity": weather.get("humidity", 60),
        "soil_ph": soil.get("pH", 6.5),
        "nitrogen": soil.get("N", 50),
        "phosphorus": soil.get("P", 25),
        "potassium": soil.get("K", 200),
        "ndvi_mean": satellite.get("ndvi_mean", 0.5),
        "ndwi_mean": satellite.get("ndwi_mean", 0.0),
        "ndmi_mean": satellite.get("ndmi_mean", 0.0),
        "yield_prediction": history.get("yield_prediction", 3000),
        "disease_probability": history.get("disease_probability", 0.1),
        "historical_loss": history.get("historical_loss", 0.1),
    }
    return score_risk(features)
