from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional
from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError

router = APIRouter()

class CreateClaimRequest(BaseModel):
    policy_id: str
    incident_date: str
    event_type: str
    description: str
    evidence_ids: list[str]

@router.get("", response_model=Envelope)
async def list_claims():
    return Envelope(
        success=True,
        data=[], 
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("", response_model=Envelope, status_code=201)
async def create_claim(req: CreateClaimRequest, idempotency_key: str = Header(..., alias="Idempotency-Key")):
    # Idempotency handling: in a real app, we would check if idempotency_key exists in DB
    return Envelope(
        success=True,
        data={"claim_id": str(uuid.uuid4()), "idempotency_key": idempotency_key, "status": "SUBMITTED"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/{id}", response_model=Envelope)
async def get_claim(id: str):
    return Envelope(
        success=True,
        data={"id": id, "status": "SUBMITTED"},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("/{id}/assess", response_model=Envelope)
async def assess_claim(id: str):
    # This would call ai_client.py get_damage_assessment
    return Envelope(
        success=True,
        data={"id": id, "status": "AI_ASSESSED", "damage_pct": 0.45},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )
