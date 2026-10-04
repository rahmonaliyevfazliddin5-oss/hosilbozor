from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User, UserRole
from app.models.review import DisputeStatus
from app.schemas.user import UserRead
from app.schemas.admin import (
    PlatformMetricsResponse,
    DisputeResolutionRequest,
    DisputeRead,
    VerificationQueueUser
)
from app.services.admin_service import admin_service

router = APIRouter(dependencies=[Depends(require_role([UserRole.ADMIN]))])


@router.get("/metrics", response_model=PlatformMetricsResponse)
def get_platform_kpis(db: Session = Depends(get_db)):
    """Returns platform KPIs: GMV, orders, active users, fill rate, and price spreads."""
    return admin_service.get_metrics(db)


@router.get("/users/verification-queue", response_model=List[VerificationQueueUser])
def list_verification_queue(db: Session = Depends(get_db)):
    """Lists unverified users waiting for moderation review."""
    users = admin_service.list_verification_queue(db)
    return [
        VerificationQueueUser(
            id=u.id,
            full_name=u.full_name,
            phone=u.phone,
            telegram_id=u.telegram_id,
            role=u.role.value if hasattr(u.role, "value") else str(u.role),
            created_at=str(u.created_at)
        )
        for u in users
    ]


@router.post("/users/{id}/verify", response_model=UserRead)
def verify_user(id: str, db: Session = Depends(get_db)):
    """Grants verified farmer/buyer status."""
    return admin_service.verify_user(db, id)


@router.get("/disputes", response_model=List[DisputeRead])
def list_disputes(db: Session = Depends(get_db)):
    """Lists all buyer/seller disputes."""
    disputes = admin_service.list_disputes(db)
    return [
        DisputeRead(
            id=d.id,
            order_id=d.order_id,
            raised_by=d.raised_by,
            reason=d.reason,
            evidence_urls=d.evidence_urls,
            status=d.status,
            resolution=d.resolution,
            created_at=str(d.created_at)
        )
        for d in disputes
    ]


@router.post("/disputes/{id}/resolve", response_model=DisputeRead)
def resolve_dispute(
    id: str,
    payload: DisputeResolutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Arbitrates dispute, triggering either fund release to seller or refund to buyer."""
    dispute = admin_service.resolve_dispute(db, current_user, id, payload)
    return DisputeRead(
        id=dispute.id,
        order_id=dispute.order_id,
        raised_by=dispute.raised_by,
        reason=dispute.reason,
        evidence_urls=dispute.evidence_urls,
        status=dispute.status,
        resolution=dispute.resolution,
        created_at=str(dispute.created_at)
    )
