from sqlalchemy import Column, String
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Crop(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "crops"

    slug = Column(String(50), unique=True, index=True, nullable=False)
    name_uz = Column(String(100), nullable=False)
    name_ru = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # vegetables, fruits, grains, legumes
    standard_unit = Column(String(20), default="kg", nullable=False)  # kg, ton
