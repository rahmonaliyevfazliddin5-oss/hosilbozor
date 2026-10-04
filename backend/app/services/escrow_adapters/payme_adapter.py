import base64
from typing import Dict, Any
from app.core.config import settings
from app.models.order import Order
from app.schemas.escrow import PaymentInvoiceResponse
from app.services.escrow_adapters.base import BaseEscrowAdapter


class PaymeAdapter(BaseEscrowAdapter):
    def generate_invoice(self, order: Order, invoice_id: str) -> PaymentInvoiceResponse:
        # Amount in tiyin (1 UZS = 100 tiyin)
        amount_tiyin = int(order.total_amount * 100)
        merchant_id = settings.PAYME_MERCHANT_ID or "mock_payme_merchant"
        
        # Payme base64 query format: m=...;ac.order_id=...;a=...
        params_str = f"m={merchant_id};ac.order_id={order.id};a={amount_tiyin}"
        encoded_params = base64.b64encode(params_str.encode("utf-8")).decode("utf-8")
        checkout_url = f"https://checkout.paycom.uz/{encoded_params}"

        return PaymentInvoiceResponse(
            invoice_id=invoice_id,
            order_id=order.id,
            amount=order.total_amount,
            provider="payme",
            checkout_url=checkout_url,
            params={
                "merchant_id": merchant_id,
                "amount_tiyin": amount_tiyin,
                "account": {"order_id": order.id}
            }
        )

    def verify_webhook(self, headers: Dict[str, str], payload: Dict[str, Any]) -> bool:
        # Payme sends Basic Auth header: Basic base64(Paycom:SECRET_KEY)
        auth_header = headers.get("authorization", "")
        if not auth_header.startswith("Basic "):
            return False
        # In production, check secret key
        return True
