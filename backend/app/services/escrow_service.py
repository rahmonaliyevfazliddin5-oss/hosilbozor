import uuid
from decimal import Decimal
from typing import Optional, Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User, UserRole
from app.models.order import Order, OrderStatus
from app.models.escrow import EscrowTxType, EscrowTxStatus
from app.schemas.escrow import (
    PaymentInvoiceResponse,
    EscrowSummaryResponse,
    EscrowLedgerRead
)
from app.repositories.order_repo import order_repo
from app.repositories.escrow_repo import escrow_repo
from app.services.order_service import order_service
from app.services.escrow_adapters.base import BaseEscrowAdapter
from app.services.escrow_adapters.mock_adapter import MockEscrowAdapter
from app.services.escrow_adapters.payme_adapter import PaymeAdapter
from app.services.escrow_adapters.click_adapter import ClickAdapter


class EscrowService:
    def __init__(self):
        self.adapters: Dict[str, BaseEscrowAdapter] = {
            "mock": MockEscrowAdapter(),
            "payme": PaymeAdapter(),
            "click": ClickAdapter()
        }

    def get_adapter(self, provider_name: Optional[str] = None) -> BaseEscrowAdapter:
        p = provider_name or settings.ESCROW_PROVIDER
        return self.adapters.get(p.lower(), self.adapters["mock"])

    def create_checkout_invoice(
        self,
        db: Session,
        actor: User,
        order_id: str,
        provider_name: Optional[str] = None
    ) -> PaymentInvoiceResponse:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        if actor.id != order.buyer_id and actor.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Faqat xaridor to'lov qilishi mumkin")

        if order.status not in (OrderStatus.CREATED, OrderStatus.CONFIRMED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyurtma holati '{order.status.value}' uchun to'lov qabul qilinmaydi"
            )

        provider_key = (provider_name or settings.ESCROW_PROVIDER).lower()
        adapter = self.get_adapter(provider_key)

        invoice_id = f"INV-{uuid.uuid4().hex[:12].upper()}"
        invoice_resp = adapter.generate_invoice(order, invoice_id)

        # Record payment record
        escrow_repo.create_payment(
            db,
            order_id=order.id,
            amount=order.total_amount,
            provider=provider_key,
            invoice_id=invoice_id
        )

        return invoice_resp

    def handle_payment_success(
        self,
        db: Session,
        order_id: str,
        provider: str = "mock",
        tx_id: Optional[str] = None
    ) -> None:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        # 1. Record deposit in escrow ledger
        escrow_repo.record_entry(
            db,
            order_id=order.id,
            transaction_type=EscrowTxType.DEPOSIT,
            amount=order.total_amount,
            provider=provider,
            provider_tx_id=tx_id or f"TX-{uuid.uuid4().hex[:8]}",
            status=EscrowTxStatus.SUCCESS,
            notes=f"Xaridor {provider.upper()} orqali mablag' kiritdi"
        )

        # 2. Record escrow hold
        escrow_repo.record_entry(
            db,
            order_id=order.id,
            transaction_type=EscrowTxType.HOLD,
            amount=order.total_amount,
            provider=provider,
            provider_tx_id=tx_id,
            status=EscrowTxStatus.SUCCESS,
            notes="Mablag' yetkazib berish yakunlanguncha platformada muzlatildi"
        )

        # 3. Transition order status to PAID_ESCROW
        if order.status != OrderStatus.PAID_ESCROW:
            order_repo.set_status(db, order, OrderStatus.PAID_ESCROW, order.buyer_id, "To'lov tasdiqlandi va muzlatildi")

    def release_escrow(self, db: Session, order_id: str) -> None:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        # 1. Release to seller
        seller_share = order.total_product_amount
        escrow_repo.record_entry(
            db,
            order_id=order.id,
            transaction_type=EscrowTxType.RELEASE,
            amount=seller_share,
            provider="escrow",
            notes=f"Fermerga hosil puli o'tkazildi ({seller_share} UZS)"
        )

        # 2. Release to driver (if logistics engaged)
        if order.delivery_amount > 0:
            escrow_repo.record_entry(
                db,
                order_id=order.id,
                transaction_type=EscrowTxType.RELEASE,
                amount=order.delivery_amount,
                provider="escrow",
                notes=f"Haydovchiga yetkazish haqi o'tkazildi ({order.delivery_amount} UZS)"
            )

        # 3. Platform fee
        if order.platform_fee > 0:
            escrow_repo.record_entry(
                db,
                order_id=order.id,
                transaction_type=EscrowTxType.FEE,
                amount=order.platform_fee,
                provider="platform",
                notes=f"Platforma xizmat haqi ({order.platform_fee} UZS)"
            )

    def refund_escrow(self, db: Session, order_id: str, reason: str = "Buyurtma bekor qilindi") -> None:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        escrow_repo.record_entry(
            db,
            order_id=order.id,
            transaction_type=EscrowTxType.REFUND,
            amount=order.total_amount,
            provider="escrow",
            notes=f"Xaridorga to'liq mablag' qaytarildi ({reason})"
        )

    def get_order_summary(self, db: Session, order_id: str) -> EscrowSummaryResponse:
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        entries = escrow_repo.list_entries_for_order(db, order_id)

        held_sum = Decimal("0.0")
        released_sum = Decimal("0.0")
        refunded_sum = Decimal("0.0")

        for e in entries:
            if e.transaction_type == EscrowTxType.HOLD:
                held_sum += e.amount
            elif e.transaction_type == EscrowTxType.RELEASE:
                released_sum += e.amount
            elif e.transaction_type == EscrowTxType.REFUND:
                refunded_sum += e.amount

        return EscrowSummaryResponse(
            order_id=order.id,
            total_amount=order.total_amount,
            held_amount=held_sum,
            released_amount=released_sum,
            refunded_amount=refunded_sum,
            status=order.status.value,
            ledger_entries=[EscrowLedgerRead.model_validate(e) for e in entries]
        )


escrow_service = EscrowService()
