from typing import Dict, Any, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.review import Dispute
from app.schemas.admin import PlatformMetricsResponse, DisputeResolutionRequest
from app.repositories.admin_repo import admin_repo
from app.repositories.order_repo import order_repo
from app.services.order_service import order_service
from app.services.escrow_service import escrow_service


class AdminService:
    def get_metrics(self, db: Session) -> PlatformMetricsResponse:
        metrics = admin_repo.get_platform_metrics(db)
        return PlatformMetricsResponse(**metrics)

    def list_verification_queue(self, db: Session) -> List[User]:
        return admin_repo.get_unverified_users(db)

    def verify_user(self, db: Session, user_id: str) -> User:
        user = admin_repo.verify_user(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")
        return user

    def list_disputes(self, db: Session) -> List[Dispute]:
        return admin_repo.get_disputes(db)

    def resolve_dispute(
        self,
        db: Session,
        admin_user: User,
        dispute_id: str,
        payload: DisputeResolutionRequest
    ) -> Dispute:
        dispute = admin_repo.resolve_dispute(
            db,
            dispute_id=dispute_id,
            admin_id=admin_user.id,
            action=payload.action,
            notes=payload.resolution_notes
        )
        if not dispute:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nizo topilmadi")

        order = order_repo.get_by_id(db, dispute.order_id)
        if order and order.status == OrderStatus.DISPUTED:
            if payload.action == "release_to_seller":
                # Disburse escrow funds to farmer
                order_repo.set_status(db, order, OrderStatus.COMPLETED, admin_user.id, f"Admin qarori: {payload.resolution_notes}")
                escrow_service.release_escrow(db, order.id)
            elif payload.action == "refund_to_buyer":
                # Refund escrow funds to buyer
                order_repo.set_status(db, order, OrderStatus.CANCELLED, admin_user.id, f"Admin qarori: {payload.resolution_notes}")
                escrow_service.refund_escrow(db, order.id, payload.resolution_notes)

        return dispute


admin_service = AdminService()
