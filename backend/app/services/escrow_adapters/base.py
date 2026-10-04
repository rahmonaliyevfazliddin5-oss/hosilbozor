from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from app.models.order import Order
from app.schemas.escrow import PaymentInvoiceResponse


class BaseEscrowAdapter(ABC):
    @abstractmethod
    def generate_invoice(self, order: Order, invoice_id: str) -> PaymentInvoiceResponse:
        pass

    @abstractmethod
    def verify_webhook(self, headers: Dict[str, str], payload: Dict[str, Any]) -> bool:
        pass
