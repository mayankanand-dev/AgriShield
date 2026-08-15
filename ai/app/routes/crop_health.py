"""Crop health detection endpoint."""
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

@router.post("/")
async def detect_crop_health(
    image: UploadFile = File(...),
    crop: str = Form(...),
    growth_stage: str = Form(...)
):
    """Detect crop health from image."""
    # TODO: Implement crop health detection
    return {
        "label": "healthy",
        "severity": 0,
        "confidence": 0.95,
        "boxes": []
    }
