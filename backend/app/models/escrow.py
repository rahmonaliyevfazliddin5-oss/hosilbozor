import enum
from sqlalchemy import Column, String, ForeignKey, Numeric, Enum, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class EscrowTxType(str, enum.Enum):
    DEPOSIT = "deposit"
    HOLD = "hold"
    RELEASE = "release"
    REFUND = "refund"
    FEE = "fee"


class EscrowTxStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class EscrowLedger(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "escrow_ledger"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    transaction_type = Column(Enum(EscrowTxType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    provider = Column(String(30), default="mock", nullable=False)  # mock, payme, click, uzum
    provider_tx_id = Column(String(100), nullable=True, index=True)
    status = Column(Enum(EscrowTxStatus), default=EscrowTxStatus.SUCCESS, nullable=False)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="escrow_entries")


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    provider = Column(String(30), default="mock", nullable=False)
    invoice_id = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(30), default="pending", nullable=False)
    payload = Column(Text, nullable=True)

    order = relationship("Order")
