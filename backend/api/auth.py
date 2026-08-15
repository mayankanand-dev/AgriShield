from fastapi import APIRouter, Depends
from pydantic import BaseModel
import uuid
from datetime import datetime
from schemas.contract import Envelope, EnvelopeMeta

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    language: str
    phone: str = ""
    email: str = ""

@router.post("/register", response_model=Envelope)
async def register(req: RegisterRequest):
    # Dummy implementation for now
    return Envelope(
        success=True,
        data={"user": {"name": req.name, "language": req.language}, "access_token": "dummy_token"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("/login", response_model=Envelope)
async def login():
    return Envelope(
        success=True,
        data={"access_token": "dummy_token", "refresh_token": "dummy_refresh"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("/refresh", response_model=Envelope)
async def refresh():
    return Envelope(
        success=True,
        data={"access_token": "dummy_token_new"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/me", response_model=Envelope)
async def me():
    return Envelope(
        success=True,
        data={"user_id": str(uuid.uuid4()), "roles": ["FARMER"]},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )
