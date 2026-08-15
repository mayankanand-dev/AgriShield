from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError
from db.session import get_db
from db.models import Claim, ClaimStatus, Farm
from services.blockchain_service import generate_tamper_proof_hash, record_hash_on_chain

router = APIRouter()

class CreateClaimRequest(BaseModel):
    policy_id: str
    incident_date: str
    event_type: str
    description: str
    evidence_ids: list[str]

@router.get("", response_model=Envelope)
async def list_claims(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Claim).order_by(Claim.incident_date.desc()))
    claims = result.scalars().all()
    
    claims_list = []
    for c in claims:
        claims_list.append({
            "id": str(c.id),
            "farm_id": str(c.farm_id) if c.farm_id else None,
            "status": c.status.value if c.status else "SUBMITTED",
            "incident_date": c.incident_date.isoformat() if c.incident_date else None,
            "event_type": c.event_type
        })
        
    return Envelope(
        success=True,
        data=claims_list,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("", response_model=Envelope, status_code=201)
async def create_claim(req: CreateClaimRequest, idempotency_key: str = Header(..., alias="Idempotency-Key"), db: AsyncSession = Depends(get_db)):
    # In a real app we'd link policy_id to a real policy. For now we link to the first farm.
    farm_result = await db.execute(select(Farm).limit(1))
    farm = farm_result.scalar_one_or_none()
    
    try:
        incident_date = datetime.fromisoformat(req.incident_date.replace("Z", "+00:00"))
    except ValueError:
        incident_date = datetime.utcnow()
        
    new_claim = Claim(
        farm_id=farm.id if farm else None,
        policy_id=uuid.UUID(req.policy_id) if len(req.policy_id) == 36 else uuid.uuid4(),
        incident_date=incident_date,
        event_type=req.event_type,
        description=req.description,
        status=ClaimStatus.SUBMITTED
    )
    
    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)
    
    return Envelope(
        success=True,
        data={"claim_id": str(new_claim.id), "idempotency_key": idempotency_key, "status": new_claim.status.value},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/{id}", response_model=Envelope)
async def get_claim(id: str, db: AsyncSession = Depends(get_db)):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID")
        )
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="NOT_FOUND", message="Claim not found")
        )
        
    return Envelope(
        success=True,
        data={
            "id": str(claim.id), 
            "status": claim.status.value if claim.status else "SUBMITTED",
            "event_type": claim.event_type,
            "damage_pct": claim.damage_pct,
            "description": claim.description
        },
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("/{id}/assess", response_model=Envelope)
async def assess_claim(id: str, db: AsyncSession = Depends(get_db)):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID")
        )
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="NOT_FOUND", message="Claim not found")
        )
        
    # Simulate AI Assessment
    claim.status = ClaimStatus.AI_ASSESSED
    claim.damage_pct = 0.45
    claim.ai_confidence = 0.92
    
    payload = {
        "claim_id": str(claim.id),
        "policy_id": str(claim.policy_id),
        "damage_pct": claim.damage_pct,
        "ai_confidence": claim.ai_confidence
    }
    canonical_hash = generate_tamper_proof_hash(payload)
    claim.canonical_hash = canonical_hash
    claim.tx_hash = await record_hash_on_chain(canonical_hash)
    
    await db.commit()
    await db.refresh(claim)
    
    return Envelope(
        success=True,
        data={
            "id": str(claim.id), 
            "status": claim.status.value, 
            "damage_pct": claim.damage_pct,
            "ai_confidence": claim.ai_confidence
        },
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/{id}/verification", response_model=Envelope)
async def verify_claim(id: str, db: AsyncSession = Depends(get_db)):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID")
        )
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return Envelope(
            success=False, data=None,
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="NOT_FOUND", message="Claim not found")
        )
        
    return Envelope(
        success=True,
        data={
            "canonical_hash": claim.canonical_hash,
            "tx_hash": claim.tx_hash,
            "status": "VERIFIED" if claim.tx_hash else "PENDING"
        },
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )
