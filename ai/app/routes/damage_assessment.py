"""Damage assessment endpoint — mock until model is trained."""
from fastapi import APIRouter, UploadFile, File, Form
from typing import List

router = APIRouter()


@router.post("/")
async def assess_damage(
    images: List[UploadFile] = File(...),
    crop: str = Form(...),
    event_type: str = Form(...),
):
    """Assess crop damage from images. Returns mock until damage model is trained."""
    return {
        "damage_pct": 0.28,
        "severity": "moderate",
        "detections": [
            {"label": event_type, "area_pct": 0.28, "confidence": 0.87}
        ],
        "confidence": 0.87,
        "model_version": "mock-damage-v1",
        "low_confidence": False,
        "inference_ms": 320,
    }
