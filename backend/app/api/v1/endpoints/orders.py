from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.order import OrderStatus
from app.schemas.order import (
    OrderCreateFromListing,
    OrderRead,
    OrderListResponse,
    OrderPickupVerificationRequest,
    OrderDeliveryVerificationRequest,
    OrderDisputeRequest,
    UserSummaryInOrder
)
from app.repositories.order_repo import order_repo
from app.services.order_service import order_service
from app.services.listing_service import listing_service

router = APIRouter()


def enrich_order_read(order, current_user: Optional[User] = None) -> OrderRead:
    buyer_summary = UserSummaryInOrder(
        id=order.buyer.id,
        full_name=order.buyer.full_name,
        phone=order.buyer.phone
    ) if order.buyer else None

    seller_summary = UserSummaryInOrder(
        id=order.seller.id,
        full_name=order.seller.full_name,
        phone=order.seller.phone
    ) if order.seller else None

    listing_read = listing_service.enrich_listing_read(order.listing) if order.listing else None

    read_item = OrderRead.model_validate(order)
    read_item.buyer = buyer_summary
    read_item.seller = seller_summary
    read_item.listing = listing_read

    # Security: only expose pickup_code to seller and driver, delivery_code to buyer and driver
    if current_user:
        if current_user.id != order.seller_id and current_user.role != UserRole.ADMIN:
            read_item.pickup_code = None
        if current_user.id != order.buyer_id and current_user.role != UserRole.ADMIN:
            read_item.delivery_code = None

    return read_item


@router.post("/from-listing", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def place_order_from_listing(
    payload: OrderCreateFromListing,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Directly creates an order against an active harvest listing (Buyer only)."""
    order = order_service.create_order_from_listing(db, current_user, payload)
    return enrich_order_read(order, current_user)


@router.get("", response_model=OrderListResponse)
def list_orders(
    status: Optional[OrderStatus] = Query(None),
    role: Optional[str] = Query(None, pattern="^(buyer|seller|all)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists orders relevant to the authenticated user."""
    total, items = order_repo.list_orders(
        db,
        user_id=current_user.id if current_user.role != UserRole.ADMIN else None,
        status=status,
        role=role,
        skip=skip,
        limit=limit
    )
    return OrderListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[enrich_order_read(o, current_user) for o in items]
    )


@router.get("/{id}", response_model=OrderRead)
def get_order_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves order with history audit trail."""
    order = order_repo.get_by_id(db, id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    if current_user.id not in (order.buyer_id, order.seller_id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")
    return enrich_order_read(order, current_user)


@router.post("/{id}/confirm", response_model=OrderRead)
def confirm_order(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Farmer accepts the order."""
    order = order_service.confirm_order(db, current_user, id)
    return enrich_order_read(order, current_user)


@router.post("/{id}/pay-escrow", response_model=OrderRead)
def pay_escrow(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buyer deposits funds into escrow hold."""
    order = order_service.pay_escrow(db, current_user, id)
    return enrich_order_read(order, current_user)


@router.post("/{id}/verify-pickup", response_model=OrderRead)
def verify_pickup(
    id: str,
    payload: OrderPickupVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validates seller's pickup code and transitions order to PICKED_UP."""
    order = order_service.verify_pickup(db, current_user, id, payload)
    return enrich_order_read(order, current_user)


@router.post("/{id}/verify-delivery", response_model=OrderRead)
def verify_delivery(
    id: str,
    payload: OrderDeliveryVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validates delivery code and photo proof, transitioning order to DELIVERED."""
    order = order_service.verify_delivery(db, current_user, id, payload)
    return enrich_order_read(order, current_user)


@router.post("/{id}/complete", response_model=OrderRead)
def complete_order(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buyer acknowledges successful delivery, concluding transaction and releasing funds."""
    order = order_service.complete_order(db, current_user, id)
    return enrich_order_read(order, current_user)


@router.post("/{id}/dispute", response_model=OrderRead)
def raise_dispute(
    id: str,
    payload: OrderDisputeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Opens a dispute and freezes funds."""
    order = order_service.raise_dispute(db, current_user, id, payload)
    return enrich_order_read(order, current_user)


@router.post("/{id}/cancel", response_model=OrderRead)
def cancel_order(
    id: str,
    reason: str = Query("Xaridor yoki sotuvchi tomonidan bekor qilindi"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancels order before fulfillment."""
    order = order_service.cancel_order(db, current_user, id, reason)
    return enrich_order_read(order, current_user)
