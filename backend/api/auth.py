from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError
from db.session import get_db
from db.models import User

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    language: str
    phone: str = ""
    email: str = ""

@router.post("/register", response_model=Envelope)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Create the user in the database
    new_user = User(
        name=req.name,
        language=req.language,
        phone=req.phone if req.phone else None,
        email=req.email if req.email else None,
        hashed_password="dummy_hash" # Real auth would hash a real password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return Envelope(
        success=True,
        data={"user": {"id": str(new_user.id), "name": new_user.name, "language": new_user.language}, "access_token": "dummy_token"},
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
async def me(db: AsyncSession = Depends(get_db)):
    # For now, just return the first user we can find to act as the current user
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    
    if not user:
        return Envelope(
            success=False,
            data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="AUTH_REQUIRED", message="No active user session")
        )
        
    return Envelope(
        success=True,
        data={"user_id": str(user.id), "name": user.name, "roles": ["FARMER"]},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )
