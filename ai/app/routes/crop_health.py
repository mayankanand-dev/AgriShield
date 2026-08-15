"""Crop health detection endpoint — mock until model is trained."""
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()


@router.post("/")
async def detect_crop_health(
    image: UploadFile = File(...),
    crop: str = Form(...),
    growth_stage: str = Form(default="vegetative"),
):
    """Detect crop health from image. Returns mock until YOLOv11 model is trained."""
    return {
        "label": "healthy",
        "severity": "none",
        "confidence": 0.91,
        "boxes": [],
        "model_version": "mock-crop-v1",
        "low_confidence": False,
        "inference_ms": 45,
    }
