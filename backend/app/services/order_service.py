from typing import Optional, Set, Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.i18n import t
from app.models.user import User, UserRole
from app.models.listing import Listing, ListingStatus
from app.models.order import Order, OrderStatus
from app.models.review import Dispute, DisputeStatus
from app.schemas.order import (
    OrderCreateFromListing,
    OrderPickupVerificationRequest,
    OrderDeliveryVerificationRequest,
    OrderDisputeRequest
)
from app.repositories.listing_repo import listing_repo
from app.repositories.order_repo import order_repo


VALID_TRANSITIONS: Dict[OrderStatus, Set[OrderStatus]] = {
    OrderStatus.CREATED: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.PAID_ESCROW, OrderStatus.CANCELLED},
    OrderStatus.PAID_ESCROW: {OrderStatus.PICKED_UP, OrderStatus.DISPUTED, OrderStatus.CANCELLED},
    OrderStatus.PICKED_UP: {OrderStatus.DELIVERED, OrderStatus.DISPUTED},
    OrderStatus.DELIVERED: {OrderStatus.COMPLETED, OrderStatus.DISPUTED},
    OrderStatus.DISPUTED: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


class OrderService:
    def create_order_from_listing(
        self,
        db: Session,
        buyer: User,
        payload: OrderCreateFromListing
    ) -> Order:
        if buyer.role != UserRole.BUYER and buyer.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", buyer.language)
            )

        listing = listing_repo.get_by_id(db, payload.listing_id)
        if not listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E'lon topilmadi")

        if listing.status != ListingStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E'lon faol emas")

        if payload.quantity < listing.min_order_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimal buyurtma miqdori: {listing.min_order_quantity}"
            )

        if payload.quantity > listing.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mavjud miqdor yetarli emas. Qolgan miqdor: {listing.quantity}"
            )

        # Deduct or reserve listing quantity
        listing.quantity -= payload.quantity
        if listing.quantity == 0:
            listing.status = ListingStatus.RESERVED
        db.commit()

        order = order_repo.create_order(
            db,
            buyer_id=buyer.id,
            seller_id=listing.farmer_id,
            quantity=payload.quantity,
            price_per_unit=listing.price_per_unit,
            delivery_amount=payload.delivery_amount,
            listing_id=listing.id
        )
        return order

    def _validate_transition(self, current_status: OrderStatus, target_status: OrderStatus) -> None:
        allowed = VALID_TRANSITIONS.get(current_status, set())
        if target_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Noto'g'ri holat o'tishi: {current_status.value} -> {target_status.value}. Ruxsat berilmagan."
            )

    def confirm_order(self, db: Session, seller: User, order_id: str) -> Order:
        order = self._get_order(db, order_id)
        if order.seller_id != seller.id and seller.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Faqat sotuvchi tasdiqlashi mumkin")

        self._validate_transition(order.status, OrderStatus.CONFIRMED)
        return order_repo.set_status(db, order, OrderStatus.CONFIRMED, seller.id, "Sotuvchi buyurtmani qabul qildi")

    def pay_escrow(self, db: Session, buyer: User, order_id: str) -> Order:
        order = self._get_order(db, order_id)
        if order.buyer_id != buyer.id and buyer.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Faqat xaridor to'lov qilishi mumkin")

        self._validate_transition(order.status, OrderStatus.PAID_ESCROW)
        return order_repo.set_status(db, order, OrderStatus.PAID_ESCROW, buyer.id, "Mablag' eskronda muzlatildi")

    def verify_pickup(
        self,
        db: Session,
        actor: User,
        order_id: str,
        payload: OrderPickupVerificationRequest
    ) -> Order:
        order = self._get_order(db, order_id)
        self._validate_transition(order.status, OrderStatus.PICKED_UP)

        if payload.pickup_code != order.pickup_code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yuk olish kodi (pickup code) noto'g'ri")

        return order_repo.set_status(db, order, OrderStatus.PICKED_UP, actor.id, "Yuk qabul qilib olindi")

    def verify_delivery(
        self,
        db: Session,
        actor: User,
        order_id: str,
        payload: OrderDeliveryVerificationRequest
    ) -> Order:
        order = self._get_order(db, order_id)
        self._validate_transition(order.status, OrderStatus.DELIVERED)

        if payload.delivery_code != order.delivery_code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yetkazish kodi (delivery code) noto'g'ri")

        notes = "Yuk yetkazib berildi va kod tasdiqlandi"
        if payload.proof_photo_url:
            notes += f" (Rasm: {payload.proof_photo_url})"

        return order_repo.set_status(db, order, OrderStatus.DELIVERED, actor.id, notes)

    def complete_order(self, db: Session, buyer: User, order_id: str) -> Order:
        order = self._get_order(db, order_id)
        if order.buyer_id != buyer.id and buyer.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Faqat xaridor qabul qilishi mumkin")

        self._validate_transition(order.status, OrderStatus.COMPLETED)
        return order_repo.set_status(db, order, OrderStatus.COMPLETED, buyer.id, "Xaridor hosil sifatini tasdiqladi, mablag' ozod qilindi")

    def raise_dispute(
        self,
        db: Session,
        actor: User,
        order_id: str,
        payload: OrderDisputeRequest
    ) -> Order:
        order = self._get_order(db, order_id)
        if actor.id not in (order.buyer_id, order.seller_id) and actor.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")

        self._validate_transition(order.status, OrderStatus.DISPUTED)

        # Create dispute record
        dispute = Dispute(
            order_id=order.id,
            raised_by=actor.id,
            reason=payload.reason,
            evidence_urls=payload.evidence_urls,
            status=DisputeStatus.OPENED
        )
        db.add(dispute)
        db.commit()

        return order_repo.set_status(db, order, OrderStatus.DISPUTED, actor.id, f"E'tiroz bildirildi: {payload.reason}")

    def cancel_order(self, db: Session, actor: User, order_id: str, reason: str = "Bekor qilindi") -> Order:
        order = self._get_order(db, order_id)
        if actor.id not in (order.buyer_id, order.seller_id) and actor.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")

        self._validate_transition(order.status, OrderStatus.CANCELLED)

        # Restore listing quantity if listing was associated
        if order.listing:
            order.listing.quantity += order.quantity
            if order.listing.status == ListingStatus.RESERVED:
                order.listing.status = ListingStatus.ACTIVE
            db.commit()

        return order_repo.set_status(db, order, OrderStatus.CANCELLED, actor.id, f"Buyurtma bekor qilindi: {reason}")

    def _get_order(self, db: Session, order_id: str) -> Order:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
        return order


order_service = OrderService()
