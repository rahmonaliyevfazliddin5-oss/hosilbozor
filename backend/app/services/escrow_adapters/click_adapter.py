import hashlib
from typing import Dict, Any
from app.core.config import settings
from app.models.order import Order
from app.schemas.escrow import PaymentInvoiceResponse
from app.services.escrow_adapters.base import BaseEscrowAdapter


class ClickAdapter(BaseEscrowAdapter):
    def generate_invoice(self, order: Order, invoice_id: str) -> PaymentInvoiceResponse:
        service_id = settings.CLICK_SERVICE_ID or "mock_service_id"
        merchant_id = settings.CLICK_MERCHANT_ID or "mock_merchant_id"
        
        checkout_url = (
            f"https://my.click.uz/services/pay"
            f"?service_id={service_id}&merchant_id={merchant_id}"
            f"&amount={order.total_amount}&transaction_param={order.id}"
            f"&return_url=https://hosilbozor.uz/orders/{order.id}"
        )

        return PaymentInvoiceResponse(
            invoice_id=invoice_id,
            order_id=order.id,
            amount=order.total_amount,
            provider="click",
            checkout_url=checkout_url,
            params={
                "service_id": service_id,
                "merchant_id": merchant_id,
                "merchant_trans_id": order.id
            }
        )

    def verify_webhook(self, headers: Dict[str, str], payload: Dict[str, Any]) -> bool:
        # Click signature is md5(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)
        return True
