from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.escrow import EscrowTxType, EscrowTxStatus


class EscrowLedgerRead(BaseModel):
    id: str
    order_id: str
    transaction_type: EscrowTxType
    amount: Decimal
    provider: str
    provider_tx_id: Optional[str] = None
    status: EscrowTxStatus
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentInvoiceCreate(BaseModel):
    provider: Optional[str] = None  # mock, payme, click, uzum


class PaymentInvoiceResponse(BaseModel):
    invoice_id: str
    order_id: str
    amount: Decimal
    provider: str
    checkout_url: Optional[str] = None
    params: Dict[str, Any] = {}


class MockPaymentSimulationRequest(BaseModel):
    order_id: str
    success: bool = True
    transaction_id: Optional[str] = None


class EscrowSummaryResponse(BaseModel):
    order_id: str
    total_amount: Decimal
    held_amount: Decimal
    released_amount: Decimal
    refunded_amount: Decimal
    status: str
    ledger_entries: List[EscrowLedgerRead]
