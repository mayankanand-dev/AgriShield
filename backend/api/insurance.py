import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.session import get_db
from db.models import User, Farm, InsurancePolicy
from schemas.insurance import QuoteRequest, PolicyCreate
from schemas.contract import Envelope, EnvelopeMeta, EnvelopeError
from services.pricing_service import calculate_premium
from services.blockchain_service import generate_tamper_proof_hash, record_hash_on_chain
from api.auth import get_current_user

router = APIRouter()

@router.post("/quote", response_model=Envelope)
async def get_quote(request: QuoteRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farm).filter(Farm.id == request.farm_id))
    farm = result.scalar_one_or_none()
    
    if not farm:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="FARM_NOT_FOUND", message="Farm not found", details={})
        )
    
    pricing = calculate_premium(area_m2=request.area_m2, crop=request.crop)
    
    return Envelope(
        success=True,
        data=pricing,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/policies", response_model=Envelope)
async def list_policies(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(InsurancePolicy))
    policies = result.scalars().all()
    
    data = []
    for p in policies:
        data.append({
            "id": str(p.id),
            "user_id": str(p.user_id),
            "farm_id": str(p.farm_id),
            "premium_amount": p.premium_amount,
            "coverage_amount": p.coverage_amount,
            "canonical_hash": p.canonical_hash,
            "tx_hash": p.tx_hash,
            "status": p.status.value if p.status else "ACTIVE",
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "start_date": p.created_at.isoformat() if p.created_at else None,
            "end_date": (p.created_at.replace(year=p.created_at.year + 1)).isoformat() if p.created_at else None
        })
        
    return Envelope(
        success=True,
        data=data,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.post("/policies", response_model=Envelope, status_code=201)
async def create_policy(
    policy_in: PolicyCreate, 
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not idempotency_key:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Idempotency-Key header is required", details={})
        )

    result = await db.execute(select(Farm).filter(Farm.id == policy_in.farm_id, Farm.user_id == current_user.id))
    farm = result.scalar_one_or_none()
    if not farm:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="FARM_NOT_FOUND", message="Farm not found or not owned by user", details={})
        )
    
    policy = InsurancePolicy(
        user_id=current_user.id,
        farm_id=farm.id,
        premium_amount=policy_in.premium_amount,
        coverage_amount=policy_in.coverage_amount
    )
    
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    
    payload = {
        "policy_id": str(policy.id),
        "user_id": str(policy.user_id),
        "farm_id": str(policy.farm_id),
        "premium": policy.premium_amount,
        "coverage": policy.coverage_amount
    }
    canonical_hash = generate_tamper_proof_hash(payload)
    
    policy.canonical_hash = canonical_hash
    policy.tx_hash = await record_hash_on_chain(canonical_hash)
    
    await db.commit()
    await db.refresh(policy)
    
    data = {
        "id": str(policy.id),
        "user_id": str(policy.user_id),
        "farm_id": str(policy.farm_id),
        "premium_amount": policy.premium_amount,
        "coverage_amount": policy.coverage_amount,
        "canonical_hash": policy.canonical_hash,
        "tx_hash": policy.tx_hash,
        "status": policy.status.value,
        "created_at": policy.created_at.isoformat() if policy.created_at else None
    }
    
    return Envelope(
        success=True,
        data=data,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/policies/{id}", response_model=Envelope)
async def get_policy(id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        policy_uuid = uuid.UUID(id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID", details={})
        )
        
    result = await db.execute(select(InsurancePolicy).filter(InsurancePolicy.id == policy_uuid, InsurancePolicy.user_id == current_user.id))
    policy = result.scalar_one_or_none()
    
    if not policy:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="POLICY_NOT_FOUND", message="Policy not found", details={})
        )
        
    data = {
        "id": str(policy.id),
        "user_id": str(policy.user_id),
        "farm_id": str(policy.farm_id),
        "premium_amount": policy.premium_amount,
        "coverage_amount": policy.coverage_amount,
        "canonical_hash": policy.canonical_hash,
        "tx_hash": policy.tx_hash,
        "status": policy.status.value if policy.status else "ACTIVE",
        "created_at": policy.created_at.isoformat() if policy.created_at else None
    }
    
    return Envelope(
        success=True,
        data=data,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )

@router.get("/policies/{id}/verification", response_model=Envelope)
async def verify_policy(id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        policy_uuid = uuid.UUID(id)
    except ValueError:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="VALIDATION_ERROR", message="Invalid UUID", details={})
        )
        
    result = await db.execute(select(InsurancePolicy).filter(InsurancePolicy.id == policy_uuid, InsurancePolicy.user_id == current_user.id))
    policy = result.scalar_one_or_none()
    
    if not policy:
        return Envelope(
            success=False, data=None, 
            meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
            error=EnvelopeError(code="POLICY_NOT_FOUND", message="Policy not found", details={})
        )
    
    data = {
        "canonical_hash": policy.canonical_hash,
        "tx_hash": policy.tx_hash,
        "status": "VERIFIED" if policy.tx_hash else "PENDING"
    }
    
    return Envelope(
        success=True,
        data=data,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None
    )
