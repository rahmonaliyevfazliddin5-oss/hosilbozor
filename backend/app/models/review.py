import enum
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class DisputeStatus(str, enum.Enum):
    OPENED = "opened"
    UNDER_REVIEW = "under_review"
    RESOLVED_RELEASE = "resolved_release"
    RESOLVED_REFUND = "resolved_refund"
    CANCELLED = "cancelled"


class Review(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    reviewee_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text, nullable=True)

    order = relationship("Order")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    reviewee = relationship("User", foreign_keys=[reviewee_id])


class Dispute(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "disputes"

    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    raised_by = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resolved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    reason = Column(Text, nullable=False)
    evidence_urls = Column(Text, nullable=True)  # JSON-encoded array or comma separated
    status = Column(Enum(DisputeStatus), default=DisputeStatus.OPENED, nullable=False, index=True)
    resolution = Column(Text, nullable=True)

    order = relationship("Order")
    raiser = relationship("User", foreign_keys=[raised_by])
    resolver = relationship("User", foreign_keys=[resolved_by])
