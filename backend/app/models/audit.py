from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class AuditLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)

    user = relationship("User")


class Notification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # order_update, price_alert, bid_received
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    channel = Column(String(20), default="telegram", nullable=False)  # telegram, sms, in_app
    is_read = Column(Boolean, default=False, nullable=False)

    user = relationship("User")
