from abc import ABC, abstractmethod
from typing import Dict, Any, List
import uuid
import httpx
from core.config import settings
from schemas.contract import AIPredictionBase

class AIClient(ABC):
    @abstractmethod
    async def get_crop_health(self, image_bytes: bytes, crop: str, growth_stage: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_damage_assessment(self, image_bytes: bytes, crop: str, event_type: str) -> Dict[str, Any]:
        pass

class MockAIClient(AIClient):
    async def get_crop_health(self, image_bytes: bytes, crop: str, growth_stage: str) -> Dict[str, Any]:
        return {
            "label": "Healthy",
            "severity": "Low",
            "boxes": [],
            "model_version": "mock-v1",
            "confidence": 0.92,
            "low_confidence": False,
            "inference_ms": 120
        }

    async def get_damage_assessment(self, image_bytes: bytes, crop: str, event_type: str) -> Dict[str, Any]:
        return {
            "damage_pct": 0.45,
            "severity": "Moderate",
            "detections": [],
            "model_version": "mock-v1",
            "confidence": 0.88,
            "low_confidence": False,
            "inference_ms": 150
        }

class HttpAIClient(AIClient):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get_crop_health(self, image_bytes: bytes, crop: str, growth_stage: str) -> Dict[str, Any]:
        # Implementation to hit the real FastAPI `ai/` folder microservice
        pass

    async def get_damage_assessment(self, image_bytes: bytes, crop: str, event_type: str) -> Dict[str, Any]:
        pass

def get_ai_client() -> AIClient:
    if settings.AI_MODE.lower() == "mock" or settings.MOCK_MODE:
        return MockAIClient()
    # Replace with real service URL in production
    return HttpAIClient("http://ai-service:8001")
