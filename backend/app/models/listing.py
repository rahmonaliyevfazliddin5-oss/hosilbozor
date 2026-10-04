import enum
from sqlalchemy import Column, String, ForeignKey, Float, Numeric, Date, Text, Boolean, Integer, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class ListingStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESERVED = "reserved"
    SOLD = "sold"
    EXPIRED = "expired"


class Listing(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "listings"

    farmer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False, index=True)
    district_id = Column(String(36), ForeignKey("districts.id"), nullable=True, index=True)
    
    quantity = Column(Numeric(12, 2), nullable=False)
    min_order_quantity = Column(Numeric(12, 2), default=1.0, nullable=False)
    price_per_unit = Column(Numeric(12, 2), nullable=False)  # in UZS
    quality_grade = Column(String(20), default="standard", nullable=False)  # premium, standard, processing
    harvest_date = Column(Date, nullable=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    description = Column(Text, nullable=True)
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE, nullable=False, index=True)

    farmer = relationship("User", foreign_keys=[farmer_id])
    crop = relationship("Crop")
    district = relationship("District")
    photos = relationship("ListingPhoto", back_populates="listing", cascade="all, delete-orphan")


class ListingPhoto(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "listing_photos"

    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False, index=True)
    photo_url = Column(String(500), nullable=False)
    is_cover = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    listing = relationship("Listing", back_populates="photos")
