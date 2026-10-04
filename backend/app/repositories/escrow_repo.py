from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.escrow import EscrowLedger, Payment, EscrowTxType, EscrowTxStatus


class EscrowRepository:
    def record_entry(
        self,
        db: Session,
        order_id: str,
        transaction_type: EscrowTxType,
        amount: Decimal,
        provider: str = "mock",
        provider_tx_id: Optional[str] = None,
        status: EscrowTxStatus = EscrowTxStatus.SUCCESS,
        notes: Optional[str] = None
    ) -> EscrowLedger:
        entry = EscrowLedger(
            order_id=order_id,
            transaction_type=transaction_type,
            amount=amount,
            provider=provider,
            provider_tx_id=provider_tx_id,
            status=status,
            notes=notes
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    def list_entries_for_order(self, db: Session, order_id: str) -> List[EscrowLedger]:
        return db.query(EscrowLedger).filter(EscrowLedger.order_id == order_id).order_by(EscrowLedger.created_at.asc()).all()

    def create_payment(
        self,
        db: Session,
        order_id: str,
        amount: Decimal,
        provider: str,
        invoice_id: str,
        payload: Optional[str] = None
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            amount=amount,
            provider=provider,
            invoice_id=invoice_id,
            status="pending",
            payload=payload
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def get_payment_by_invoice(self, db: Session, invoice_id: str) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.invoice_id == invoice_id).first()

    def update_payment_status(self, db: Session, payment: Payment, new_status: str) -> Payment:
        payment.status = new_status
        db.commit()
        db.refresh(payment)
        return payment


escrow_repo = EscrowRepository()
