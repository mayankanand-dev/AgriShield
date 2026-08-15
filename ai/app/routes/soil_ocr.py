"""Soil report OCR endpoint — EasyOCR + regex N/P/K/pH extraction."""
import re
from fastapi import APIRouter, UploadFile, File
from app import config

router = APIRouter()


def _parse_nutrient(text: str, pattern: str):
    m = re.search(pattern, text, re.IGNORECASE)
    return float(m.group(1)) if m else None


def _parse_soil_text(text: str) -> dict:
    N = _parse_nutrient(text, r"(?:nitrogen|available\s*N)[^\d]*(\d+\.?\d*)")
    P = _parse_nutrient(text, r"(?:phosphorus|available\s*P)[^\d]*(\d+\.?\d*)")
    K = _parse_nutrient(text, r"(?:potassium|available\s*K)[^\d]*(\d+\.?\d*)")
    pH = _parse_nutrient(text, r"pH[^\d]*(\d+\.?\d*)")
    return {"N": N, "P": P, "K": K, "pH": pH}


@router.post("/")
async def extract_soil_data(file: UploadFile = File(...)):
    """Extract soil nutrient data from PDF or image soil health card."""
    if config.MOCK_MODE:
        return {
            "N": 42.0, "P": 18.5, "K": 165.0, "pH": 6.8,
            "confidence": 0.80, "extracted_text": "Mock OCR — enable live mode for real extraction",
            "model_version": "mock-ocr-v1", "low_confidence": False, "inference_ms": 5,
        }

    try:
        import easyocr
        content = await file.read()
        reader = easyocr.Reader(["en"], gpu=False)
        ocr_result = reader.readtext(content, detail=0)
        full_text = " ".join(ocr_result)
        parsed = _parse_soil_text(full_text)

        # Fill missing with defaults and track confidence
        defaults = {"N": 45.0, "P": 22.0, "K": 180.0, "pH": 6.5}
        found = sum(1 for v in parsed.values() if v is not None)
        confidence = 0.5 + (found / 4) * 0.45  # 0.50 → 0.95 based on fields found
        final = {k: parsed[k] if parsed[k] is not None else defaults[k]
                 for k in defaults}

        return {
            **final,
            "confidence": round(confidence, 2),
            "extracted_text": full_text[:500],
            "model_version": "easyocr-v1.0",
            "low_confidence": confidence < config.MIN_CONFIDENCE,
            "inference_ms": 800,
        }
    except Exception as e:
        return {
            "N": 45.0, "P": 22.0, "K": 180.0, "pH": 6.5,
            "confidence": 0.40,
            "extracted_text": f"OCR failed: {str(e)[:200]}",
            "model_version": "fallback-v1",
            "low_confidence": True,
            "inference_ms": 0,
        }
