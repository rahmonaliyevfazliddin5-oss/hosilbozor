from sqlalchemy import Column, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class MarketPrice(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "market_prices"

    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False, index=True)
    region_id = Column(String(36), ForeignKey("regions.id"), nullable=False, index=True)
    market_name = Column(String(120), nullable=False)  # e.g. "Qo'yliq", "Parkent", "Samarqand Siyob"
    min_price = Column(Numeric(12, 2), nullable=False)
    max_price = Column(Numeric(12, 2), nullable=False)
    avg_price = Column(Numeric(12, 2), nullable=False)
    recorded_date = Column(Date, nullable=False, index=True)

    crop = relationship("Crop")
    region = relationship("Region")


class PriceAlert(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "price_alerts"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False, index=True)
    region_id = Column(String(36), ForeignKey("regions.id"), nullable=True)
    target_price = Column(Numeric(12, 2), nullable=False)
    condition = Column(String(10), default="below", nullable=False)  # "below" or "above"

    user = relationship("User")
    crop = relationship("Crop")
