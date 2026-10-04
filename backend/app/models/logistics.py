import enum
from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Float, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class JobStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class BidStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class DeliveryJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "delivery_jobs"

    order_id = Column(String(36), ForeignKey("orders.id"), unique=True, nullable=False, index=True)
    driver_id = Column(String(36), ForeignKey("driver_profiles.id"), nullable=True, index=True)
    pickup_district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    delivery_district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    
    proposed_price = Column(Numeric(12, 2), nullable=True)
    agreed_price = Column(Numeric(12, 2), nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.OPEN, nullable=False, index=True)
    
    pickup_proof_url = Column(String(500), nullable=True)
    delivery_proof_url = Column(String(500), nullable=True)

    order = relationship("Order", back_populates="delivery_job")
    driver = relationship("DriverProfile")
    bids = relationship("DeliveryBid", back_populates="job", cascade="all, delete-orphan")


class DeliveryBid(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "delivery_bids"

    job_id = Column(String(36), ForeignKey("delivery_jobs.id"), nullable=False, index=True)
    driver_id = Column(String(36), ForeignKey("driver_profiles.id"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    
    bid_amount = Column(Numeric(12, 2), nullable=False)
    estimated_hours = Column(Integer, nullable=True)
    status = Column(Enum(BidStatus), default=BidStatus.PENDING, nullable=False)

    job = relationship("DeliveryJob", back_populates="bids")
    driver = relationship("DriverProfile")
    vehicle = relationship("Vehicle")
