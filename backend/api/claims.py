from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.session import get_db
from db.models import Claim, ClaimStatus, ClaimEventType, Farm, User, UserRole, Notification, NotificationType, InsurancePolicy
from services.blockchain_service import generate_tamper_proof_hash, record_hash_on_chain
from services.ai_client import get_ai_client
from api.auth import get_current_user, get_admin_user, _ok, _error

router = APIRouter()

class CreateClaimRequest(BaseModel):
    policy_id: str
    incident_date: str
    event_type: str
    description: str
    evidence_ids: list[str]

class ReviewClaimRequest(BaseModel):
    action: str

def _serialize_claim(c: Claim, include_farmer: bool = False):
    data = {
        "id": str(c.id),
        "policy_id": str(c.policy_id) if c.policy_id else None,
        "farm_id": str(c.farm_id) if c.farm_id else None,
        "status": c.status.value if c.status else "SUBMITTED",
        "event_type": c.event_type.value if hasattr(c.event_type, "value") else c.event_type,
        "damage_pct": c.damage_pct,
        "ai_confidence": c.ai_confidence,
        "description": c.description,
        "evidence_ids": [str(eid) for eid in (c.evidence_ids or [])],
        "created_at": c.created_at.isoformat() if c.created_at else None
    }
    if include_farmer and c.user:
        data["farmer"] = {
            "id": str(c.user.id),
            "name": c.user.name,
            "phone": c.user.phone
        }
    return data

@router.get("")
async def list_claims(
    page: int = 1, 
    page_size: int = 50, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    query = select(Claim).options(selectinload(Claim.user)).order_by(Claim.created_at.desc(), Claim.id)
    
    if current_user.role != UserRole.ADMIN:
        query = query.where(Claim.user_id == current_user.id)
        
    query = query.limit(page_size).offset(offset)
    result = await db.execute(query)
    claims = result.scalars().all()
    
    is_admin = current_user.role == UserRole.ADMIN
    return _ok([_serialize_claim(c, include_farmer=is_admin) for c in claims])

@router.post("", status_code=201)
async def create_claim(
    req: CreateClaimRequest, 
    idempotency_key: str = Header(..., alias="Idempotency-Key"), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        policy_uuid = uuid.UUID(req.policy_id)
        policy = await db.get(InsurancePolicy, policy_uuid)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid policy UUID")
        
    if not policy:
        return _error("NOT_FOUND", "Policy not found", 404)
        
    if policy.user_id != current_user.id:
        return _error("FORBIDDEN", "Not allowed to file claim for this policy", 403)
        
    try:
        evidence_uuids = [uuid.UUID(eid) for eid in req.evidence_ids]
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid evidence UUID")
        
    # Check idempotency? For now just create.
    new_claim = Claim(
        user_id=current_user.id,
        farm_id=policy.farm_id,
        policy_id=policy.id,
        event_type=req.event_type,
        description=req.description,
        evidence_ids=evidence_uuids,
        status=ClaimStatus.SUBMITTED
    )
    
    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)
    
    return _ok({"claim_id": str(new_claim.id), "idempotency_key": idempotency_key, "status": new_claim.status.value})

@router.get("/{id}")
async def get_claim(
    id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return _error("NOT_FOUND", "Claim not found", 404)
        
    if current_user.role != UserRole.ADMIN and claim.user_id != current_user.id:
        return _error("FORBIDDEN", "Not allowed to view this claim", 403)
        
    is_admin = current_user.role == UserRole.ADMIN
    return _ok(_serialize_claim(claim, include_farmer=is_admin))

@router.post("/{id}/assess")
async def assess_claim(
    id: str, 
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")

    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return _error("NOT_FOUND", "Claim not found", 404)

    ai_client = get_ai_client()
    try:
        # In a real setup, we'd fetch the file bytes from `claim.evidence_ids[0]`
        _placeholder = bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10])
        ai_result = await ai_client.get_damage_assessment(
            image_bytes=_placeholder,
            crop="unknown",
            event_type=claim.event_type.value if hasattr(claim.event_type, "value") else claim.event_type,
        )
    except Exception as ai_err:
        return _error("AI_UNAVAILABLE", str(ai_err), 500)

    claim.status = ClaimStatus.AI_ASSESSED
    claim.damage_pct = ai_result.get("damage_pct", 0.0)
    claim.ai_confidence = ai_result.get("confidence", 0.0)

    payload = {
        "claim_id": str(claim.id),
        "policy_id": str(claim.policy_id),
        "damage_pct": claim.damage_pct,
        "ai_confidence": claim.ai_confidence,
        "model_version": ai_result.get("model_version", "unknown"),
    }
    canonical_hash = generate_tamper_proof_hash(payload)
    claim.canonical_hash = canonical_hash
    claim.tx_hash = await record_hash_on_chain(canonical_hash)

    # Add notification for the farmer
    notif = Notification(
        user_id=claim.user_id,
        type=NotificationType.CLAIM_STATUS,
        ref_id=claim.id,
        message=f"Your claim has been AI assessed with {claim.damage_pct}% damage."
    )
    db.add(notif)

    await db.commit()
    await db.refresh(claim)

    return _ok({
        "id": str(claim.id),
        "status": claim.status.value,
        "damage_pct": claim.damage_pct,
        "ai_confidence": claim.ai_confidence,
        "model_version": ai_result.get("model_version"),
        "tx_hash": claim.tx_hash,
    })

@router.get("/{id}/verification")
async def verify_claim(
    id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return _error("NOT_FOUND", "Claim not found", 404)
        
    return _ok({
        "canonical_hash": claim.canonical_hash,
        "tx_hash": claim.tx_hash,
        "status": "VERIFIED" if claim.tx_hash else "PENDING"
    })

@router.post("/{id}/review")
async def review_claim(
    id: str, 
    req: ReviewClaimRequest, 
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    try:
        claim_uuid = uuid.UUID(id)
    except ValueError:
        return _error("VALIDATION_ERROR", "Invalid UUID")
        
    claim = await db.get(Claim, claim_uuid)
    if not claim:
        return _error("NOT_FOUND", "Claim not found", 404)
        
    if req.action == "APPROVE":
        claim.status = ClaimStatus.APPROVED
    elif req.action == "REJECT":
        claim.status = ClaimStatus.REJECTED
    else:
        return _error("VALIDATION_ERROR", "Invalid action")
        
    claim.reviewed_by = current_admin.id
    claim.reviewed_at = datetime.utcnow()
    
    # Add notification
    notif = Notification(
        user_id=claim.user_id,
        type=NotificationType.CLAIM_STATUS,
        ref_id=claim.id,
        message=f"Your claim has been {claim.status.value}."
    )
    db.add(notif)

    await db.commit()
    await db.refresh(claim)
    
    return _ok({
        "id": str(claim.id), 
        "status": claim.status.value,
        "event_type": claim.event_type.value if hasattr(claim.event_type, "value") else claim.event_type,
        "damage_pct": claim.damage_pct,
        "description": claim.description
    })
