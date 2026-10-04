import enum
from sqlalchemy import Column, String, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    PAID_ESCROW = "paid_escrow"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    order_number = Column(String(50), unique=True, index=True, nullable=False)
    buyer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    seller_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=True)
    offer_id = Column(String(36), ForeignKey("offers.id"), nullable=True)
    
    quantity = Column(Numeric(12, 2), nullable=False)
    price_per_unit = Column(Numeric(12, 2), nullable=False)
    total_product_amount = Column(Numeric(12, 2), nullable=False)
    delivery_amount = Column(Numeric(12, 2), default=0.0, nullable=False)
    platform_fee = Column(Numeric(12, 2), default=0.0, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False, index=True)
    pickup_code = Column(String(10), nullable=True)
    delivery_code = Column(String(10), nullable=True)

    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])
    listing = relationship("Listing")
    events = relationship("OrderEvent", back_populates="order", cascade="all, delete-orphan")
    delivery_job = relationship("DeliveryJob", back_populates="order", uselist=False, cascade="all, delete-orphan")
    escrow_entries = relationship("EscrowLedger", back_populates="order", cascade="all, delete-orphan")


class OrderEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_events"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=False)
    triggered_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="events")
    user = relationship("User")
