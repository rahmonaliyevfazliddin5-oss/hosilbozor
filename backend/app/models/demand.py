import enum
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class DemandStatus(str, enum.Enum):
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class OfferStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class DemandRequest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "demand_requests"

    buyer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False, index=True)
    destination_district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    
    target_quantity = Column(Numeric(12, 2), nullable=False)
    max_price_per_unit = Column(Numeric(12, 2), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(DemandStatus), default=DemandStatus.ACTIVE, nullable=False, index=True)

    buyer = relationship("User", foreign_keys=[buyer_id])
    crop = relationship("Crop")
    destination_district = relationship("District")
    offers = relationship("Offer", back_populates="demand", cascade="all, delete-orphan")


class Offer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "offers"

    demand_id = Column(String(36), ForeignKey("demand_requests.id"), nullable=False, index=True)
    farmer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    offered_price_per_unit = Column(Numeric(12, 2), nullable=False)
    offered_quantity = Column(Numeric(12, 2), nullable=False)
    status = Column(Enum(OfferStatus), default=OfferStatus.PENDING, nullable=False)
    notes = Column(Text, nullable=True)

    demand = relationship("DemandRequest", back_populates="offers")
    farmer = relationship("User", foreign_keys=[farmer_id])
