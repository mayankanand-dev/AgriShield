from fastapi import APIRouter
import uuid
from datetime import datetime
from schemas.contract import Envelope, EnvelopeMeta

router = APIRouter()

# Simple in-memory list for demo (no DB table yet)
_NOTIFICATIONS: list = [
    {
        "id": "notif-welcome",
        "title": "Welcome to AgriShield",
        "message": "Your farm insurance dashboard is active. Register your first farm to get started.",
        "is_read": False,
        "created_at": datetime.utcnow().isoformat(),
    }
]


@router.get("", response_model=Envelope)
async def list_notifications():
    return Envelope(
        success=True,
        data=_NOTIFICATIONS,
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None,
    )


@router.post("/{id}/read", response_model=Envelope)
async def mark_notification_read(id: str):
    for n in _NOTIFICATIONS:
        if n["id"] == id:
            n["is_read"] = True
            break
    return Envelope(
        success=True,
        data={"id": id, "is_read": True},
        meta=EnvelopeMeta(request_id=uuid.uuid4(), timestamp=datetime.utcnow()),
        error=None,
    )
