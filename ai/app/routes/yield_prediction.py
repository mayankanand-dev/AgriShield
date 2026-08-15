"""Yield prediction endpoint — calls trained RandomForest model."""
from fastapi import APIRouter, Body
from app import config
from inference.yield_prediction import predict_yield

router = APIRouter()


@router.post("/")
async def predict_yield_endpoint(
    crop: str = Body(...),
    area_ha: float = Body(...),
    sowing_date: str = Body(default="2026-06-01"),
    # Weather features
    rainfall: float = Body(default=80.0),
    rainfall_7d: float = Body(default=20.0),
    rainfall_30d: float = Body(default=80.0),
    temp_mean: float = Body(default=25.0),
    temp_max: float = Body(default=32.0),
    temp_min: float = Body(default=18.0),
    humidity: float = Body(default=60.0),
    wind_speed: float = Body(default=10.0),
    # Soil features
    soil_ph: float = Body(default=6.5),
    nitrogen: float = Body(default=50.0),
    phosphorus: float = Body(default=25.0),
    potassium: float = Body(default=200.0),
    organic_carbon: float = Body(default=0.5),
    # Satellite indices
    ndvi_mean: float = Body(default=0.5),
    ndvi_min: float = Body(default=0.3),
    ndvi_max: float = Body(default=0.7),
    ndvi_std: float = Body(default=0.1),
    ndwi_mean: float = Body(default=0.0),
    ndwi_min: float = Body(default=-0.2),
    ndwi_max: float = Body(default=0.2),
    ndmi_mean: float = Body(default=0.0),
    ndmi_min: float = Body(default=-0.2),
    ndmi_max: float = Body(default=0.2),
    # Context / derived
    growth_stage: float = Body(default=0.5),
    sowing_delay_days: float = Body(default=0.0),
    heat_stress_days: float = Body(default=0.0),
    excessive_rainfall_index: float = Body(default=0.0),
    disease_probability: float = Body(default=0.1),
    historical_loss: float = Body(default=0.1),
):
    """Predict crop yield. MOCK_MODE returns fixed demo values."""
    if config.MOCK_MODE:
        return {
            "yield_value": 3200.0, "unit": "kg/ha",
            "confidence": 0.82, "model_version": "mock-v1",
            "low_confidence": False, "inference_ms": 5,
        }

    features = {
        "crop": crop, "area_ha": area_ha,
        "rainfall": rainfall, "rainfall_7d": rainfall_7d,
        "rainfall_30d": rainfall_30d, "temp_mean": temp_mean,
        "temp_max": temp_max, "temp_min": temp_min,
        "humidity": humidity, "wind_speed": wind_speed,
        "soil_ph": soil_ph, "nitrogen": nitrogen,
        "phosphorus": phosphorus, "potassium": potassium,
        "organic_carbon": organic_carbon,
        "ndvi_mean": ndvi_mean, "ndvi_min": ndvi_min,
        "ndvi_max": ndvi_max, "ndvi_std": ndvi_std,
        "ndwi_mean": ndwi_mean, "ndwi_min": ndwi_min,
        "ndwi_max": ndwi_max,
        "ndmi_mean": ndmi_mean, "ndmi_min": ndmi_min,
        "ndmi_max": ndmi_max,
        "growth_stage": growth_stage,
        "sowing_delay_days": sowing_delay_days,
        "heat_stress_days": heat_stress_days,
        "excessive_rainfall_index": excessive_rainfall_index,
        "disease_probability": disease_probability,
        "historical_loss": historical_loss,
    }
    return predict_yield(features)
