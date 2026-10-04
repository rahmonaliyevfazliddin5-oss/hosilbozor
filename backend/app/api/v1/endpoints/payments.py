from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.order import Order
from app.schemas.escrow import (
    PaymentInvoiceCreate,
    PaymentInvoiceResponse,
    MockPaymentSimulationRequest,
    EscrowSummaryResponse
)
from app.repositories.order_repo import order_repo
from app.services.escrow_service import escrow_service

router = APIRouter()


@router.post("/orders/{order_id}/checkout", response_model=PaymentInvoiceResponse)
def create_checkout_invoice(
    order_id: str,
    payload: Optional[PaymentInvoiceCreate] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generates escrow payment checkout link for an order (Buyer only)."""
    provider = payload.provider if payload else None
    return escrow_service.create_checkout_invoice(db, current_user, order_id, provider)


@router.post("/mock/simulate", status_code=status.HTTP_200_OK)
def simulate_mock_payment(
    payload: MockPaymentSimulationRequest,
    db: Session = Depends(get_db)
):
    """Sandbox simulation endpoint to trigger successful payment deposit in dev."""
    if payload.success:
        escrow_service.handle_payment_success(
            db,
            order_id=payload.order_id,
            provider="mock",
            tx_id=payload.transaction_id
        )
        return {"success": True, "message": "To'lov muvaffaqiyatli qabul qilindi va eskronda muzlatildi"}
    else:
        return {"success": False, "message": "To'lov bekor qilindi"}


@router.post("/webhook/payme")
async def payme_webhook(request: Request, db: Session = Depends(get_db)):
    """Idempotent Payme JSON-RPC webhook."""
    data = await request.json()
    method = data.get("method")
    params = data.get("params", {})
    account = params.get("account", {})
    order_id = account.get("order_id")

    if method == "CheckPerformTransaction":
        order = order_repo.get_by_id(db, order_id) if order_id else None
        if not order:
            return {"error": {"code": -31050, "message": {"uz": "Buyurtma topilmadi"}}}
        return {"result": {"allow": True}}

    elif method == "PerformTransaction":
        if order_id:
            escrow_service.handle_payment_success(
                db,
                order_id=order_id,
                provider="payme",
                tx_id=params.get("id")
            )
        return {"result": {"perform_time": 1700000000, "transaction": params.get("id"), "state": 2}}

    return {"result": {"success": True}}


@router.post("/webhook/click")
async def click_webhook(request: Request, db: Session = Depends(get_db)):
    """Idempotent Click Prepare/Complete webhook."""
    form_data = await request.form()
    order_id = form_data.get("merchant_trans_id")
    action = form_data.get("action")
    click_trans_id = form_data.get("click_trans_id")

    if action == "1":  # Complete
        if order_id:
            escrow_service.handle_payment_success(
                db,
                order_id=order_id,
                provider="click",
                tx_id=click_trans_id
            )
        return {"error": 0, "error_note": "Success", "click_trans_id": click_trans_id, "merchant_trans_id": order_id}

    return {"error": 0, "error_note": "Success"}


@router.get("/orders/{order_id}/ledger", response_model=EscrowSummaryResponse)
def get_order_escrow_ledger(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves full escrow audit ledger showing holds, releases, and fees."""
    order = order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    if current_user.id not in (order.buyer_id, order.seller_id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")

    return escrow_service.get_order_summary(db, order_id)
