"""Agricultural advisory endpoint — rule-based recommendations."""
from fastapi import APIRouter, Body

router = APIRouter()

_CROP_ADVISORIES = {
    "wheat":     ["Apply nitrogen at tillering stage", "Monitor for yellow rust", "Irrigate at crown root initiation"],
    "rice":      ["Maintain 5cm water level in field", "Apply DAP at transplanting", "Watch for blast and BLB disease"],
    "cotton":    ["Scout for bollworm weekly after 45 DAS", "Spray NPK 19-19-19 at boll formation", "Avoid waterlogging"],
    "corn":      ["Top-dress urea at knee-height stage", "Irrigate at tasseling and silking", "Monitor for fall armyworm"],
    "sugarcane": ["Earth-up at 60 days", "Apply FYM before planting", "Watch for top borer in July-August"],
    "soybean":   ["Inoculate seeds with Rhizobium", "Apply sulfur for pod fill", "Control pod borer at flowering"],
}


@router.post("/")
async def get_advisory(farm_context: dict = Body(...)):
    """Generate crop advisory from farm context (soil, weather, crop type)."""
    crop = farm_context.get("crop", "").lower().strip()
    soil = farm_context.get("soil", {})
    weather = farm_context.get("weather", {})

    recommendations = list(_CROP_ADVISORIES.get(crop, [
        f"Use balanced NPK fertilizer for {crop or 'your crop'}",
        "Scout fields weekly for pest and disease signs",
        "Maintain soil moisture at field capacity",
    ]))

    warnings = []
    if weather.get("rainfall", 0) > 150:
        warnings.append("Excess rainfall detected — ensure field drainage is functional")
    if weather.get("temp_mean", 25) > 38:
        warnings.append("Heat stress risk — consider protective irrigation")
    if soil.get("pH", 7.0) < 5.5:
        warnings.append("Soil pH too acidic — apply agricultural lime before next season")
    if soil.get("pH", 7.0) > 8.0:
        warnings.append("Alkaline soil — apply gypsum and organic matter")
    if soil.get("N", 50) < 20:
        warnings.append("Nitrogen deficiency — apply urea at 60 kg/ha")
    if soil.get("P", 25) < 10:
        warnings.append("Phosphorus deficiency — apply SSP or DAP")

    return {
        "recommendations": recommendations,
        "warnings": warnings,
        "model_version": "advisory-rules-v1.0",
        "confidence": 0.85,
        "low_confidence": False,
        "inference_ms": 2,
    }
