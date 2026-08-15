"""Soil report OCR endpoint."""
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def extract_soil_data(file: UploadFile = File(...)):
    """Extract soil data from PDF/image."""
    # TODO: Implement soil OCR
    return {
        "N": 0,
        "P": 0,
        "K": 0,
        "pH": 0,
        "confidence": 0.80,
        "extracted_text": ""
    }
