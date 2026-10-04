from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Region(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "regions"

    code = Column(String(20), unique=True, index=True, nullable=False)
    name_uz = Column(String(100), nullable=False)
    name_ru = Column(String(100), nullable=False)

    districts = relationship("District", back_populates="region", cascade="all, delete-orphan")


class District(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "districts"

    region_id = Column(String(36), ForeignKey("regions.id"), nullable=False, index=True)
    name_uz = Column(String(100), nullable=False)
    name_ru = Column(String(100), nullable=False)

    region = relationship("Region", back_populates="districts")
