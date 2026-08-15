from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from core.config import settings

from api import auth, farms, soil, weather, satellite, ai, insurance, claims, notifications, admin

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Generic exception handler to wrap in standard envelope
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    import uuid
    from datetime import datetime
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "meta": {
                "request_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat()
            },
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc),
                "details": {}
            }
        }
    )

@app.get("/health")
def health_check():
    return {"status": "OK"}

api_router = FastAPI()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(farms.router, prefix="/farms", tags=["farms"])
api_router.include_router(soil.router, prefix="/soil", tags=["soil"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(satellite.router, prefix="/satellite", tags=["satellite"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(insurance.router, prefix="/insurance", tags=["insurance"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

app.mount(settings.API_V1_STR, api_router)
