from typing import Dict, Any
from app.models.order import Order
from app.schemas.escrow import PaymentInvoiceResponse
from app.services.escrow_adapters.base import BaseEscrowAdapter


class MockEscrowAdapter(BaseEscrowAdapter):
    def generate_invoice(self, order: Order, invoice_id: str) -> PaymentInvoiceResponse:
        return PaymentInvoiceResponse(
            invoice_id=invoice_id,
            order_id=order.id,
            amount=order.total_amount,
            provider="mock",
            checkout_url=f"/api/v1/payments/mock/simulate?order_id={order.id}&invoice_id={invoice_id}",
            params={"mode": "development_sandbox"}
        )

    def verify_webhook(self, headers: Dict[str, str], payload: Dict[str, Any]) -> bool:
        return True
