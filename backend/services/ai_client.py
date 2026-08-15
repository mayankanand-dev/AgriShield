from abc import ABC, abstractmethod
from typing import Dict, Any
import httpx
from core.config import settings


class AIClient(ABC):
    @abstractmethod
    async def get_crop_health(self, image_bytes: bytes, crop: str, growth_stage: str) -> Dict[str, Any]: pass

    @abstractmethod
    async def get_damage_assessment(self, image_bytes: bytes, crop: str, event_type: str) -> Dict[str, Any]: pass

    @abstractmethod
    async def get_yield_prediction(self, crop: str, area_ha: float, weather: dict, soil: dict, satellite: dict) -> Dict[str, Any]: pass

    @abstractmethod
    async def get_risk_score(self, crop: str, area_ha: float, weather: dict, soil: dict, satellite: dict, history: dict) -> Dict[str, Any]: pass

    @abstractmethod
    async def get_soil_ocr(self, file_bytes: bytes, filename: str) -> Dict[str, Any]: pass

    @abstractmethod
    async def get_advisory(self, farm_context: dict) -> Dict[str, Any]: pass


class MockAIClient(AIClient):
    async def get_crop_health(self, image_bytes, crop, growth_stage):
        return {
            "label": "Healthy", "severity": "none", "boxes": [],
            "model_version": "mock-v1", "confidence": 0.92,
            "low_confidence": False, "inference_ms": 10,
        }

    async def get_damage_assessment(self, image_bytes, crop, event_type):
        return {
            "damage_pct": 0.28, "severity": "moderate",
            "detections": [{"label": event_type, "area_pct": 0.28, "confidence": 0.87}],
            "model_version": "mock-v1", "confidence": 0.87,
            "low_confidence": False, "inference_ms": 12,
        }

    async def get_yield_prediction(self, crop, area_ha, weather, soil, satellite):
        return {
            "yield_value": 3200.0, "unit": "kg/ha",
            "model_version": "mock-v1", "confidence": 0.82,
            "low_confidence": False, "inference_ms": 5,
        }

    async def get_risk_score(self, crop, area_ha, weather, soil, satellite, history):
        return {
            "risk_score": 0.35, "risk_band": "medium", "factors": [],
            "model_version": "mock-v1", "confidence": 0.88,
            "low_confidence": False, "inference_ms": 3,
        }

    async def get_soil_ocr(self, file_bytes, filename):
        return {
            "N": 42.0, "P": 18.5, "K": 165.0, "pH": 6.8,
            "confidence": 0.80, "extracted_text": "Mock OCR",
            "model_version": "mock-v1", "low_confidence": False, "inference_ms": 5,
        }

    async def get_advisory(self, farm_context):
        return {
            "recommendations": ["Apply balanced NPK", "Monitor crop weekly"],
            "warnings": [],
            "model_version": "mock-v1", "confidence": 0.85,
            "low_confidence": False, "inference_ms": 2,
        }


class HttpAIClient(AIClient):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_crop_health(self, image_bytes: bytes, crop: str, growth_stage: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/crop-health",
                files={"image": ("image.jpg", image_bytes, "image/jpeg")},
                data={"crop": crop, "growth_stage": growth_stage},
            )
            r.raise_for_status()
            return r.json()

    async def get_damage_assessment(self, image_bytes: bytes, crop: str, event_type: str):
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/damage-assessment",
                files={"images": ("image.jpg", image_bytes, "image/jpeg")},
                data={"crop": crop, "event_type": event_type},
            )
            r.raise_for_status()
            return r.json()

    async def get_yield_prediction(self, crop: str, area_ha: float, weather: dict, soil: dict, satellite: dict):
        payload = {
            "crop": crop,
            "area_ha": area_ha,
            "sowing_date": "2026-06-01",
            # Flatten weather
            "rainfall": weather.get("rainfall", 80),
            "rainfall_7d": weather.get("rainfall_7d", 20),
            "rainfall_30d": weather.get("rainfall_30d", 80),
            "temp_mean": weather.get("temp_mean", 25),
            "temp_max": weather.get("temp_max", 32),
            "temp_min": weather.get("temp_min", 18),
            "humidity": weather.get("humidity", 60),
            "wind_speed": weather.get("wind_speed", 10),
            # Flatten soil
            "soil_ph": soil.get("pH", 6.5),
            "nitrogen": soil.get("N", 50),
            "phosphorus": soil.get("P", 25),
            "potassium": soil.get("K", 200),
            "organic_carbon": soil.get("organic_carbon", 0.5),
            # Flatten satellite
            "ndvi_mean": satellite.get("ndvi_mean", 0.5),
            "ndvi_min": satellite.get("ndvi_min", 0.3),
            "ndvi_max": satellite.get("ndvi_max", 0.7),
            "ndvi_std": satellite.get("ndvi_std", 0.1),
            "ndwi_mean": satellite.get("ndwi_mean", 0.0),
            "ndwi_min": satellite.get("ndwi_min", -0.2),
            "ndwi_max": satellite.get("ndwi_max", 0.2),
            "ndmi_mean": satellite.get("ndmi_mean", 0.0),
            "ndmi_min": satellite.get("ndmi_min", -0.2),
            "ndmi_max": satellite.get("ndmi_max", 0.2),
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(f"{self.base_url}/v1/yield-prediction", json=payload)
            r.raise_for_status()
            return r.json()

    async def get_risk_score(self, crop: str, area_ha: float, weather: dict, soil: dict, satellite: dict, history: dict):
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/risk-score",
                json={
                    "crop": crop,
                    "area_ha": area_ha,
                    "weather": weather,
                    "soil": soil,
                    "satellite": satellite,
                    "history": history,
                },
            )
            r.raise_for_status()
            return r.json()

    async def get_soil_ocr(self, file_bytes: bytes, filename: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/soil-ocr",
                files={"file": (filename, file_bytes, "application/octet-stream")},
            )
            r.raise_for_status()
            return r.json()

    async def get_advisory(self, farm_context: dict):
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(f"{self.base_url}/v1/advisory", json=farm_context)
            r.raise_for_status()
            return r.json()


def get_ai_client() -> AIClient:
    if settings.AI_MODE.lower() == "mock" or settings.MOCK_MODE:
        return MockAIClient()
    return HttpAIClient(settings.AI_SERVICE_URL)
