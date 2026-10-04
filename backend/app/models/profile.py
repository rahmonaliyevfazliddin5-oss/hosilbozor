from sqlalchemy import Column, String, ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class FarmerProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "farmer_profiles"

    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    region_id = Column(String(36), ForeignKey("regions.id"), nullable=True)
    district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    farm_name = Column(String(120), nullable=True)
    rating = Column(Float, default=5.0, nullable=False)
    total_deals = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="farmer_profile")


class BuyerProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "buyer_profiles"

    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    company_name = Column(String(150), nullable=True)
    buyer_type = Column(String(50), default="wholesale", nullable=False)  # wholesale, restaurant, retailer, personal
    rating = Column(Float, default=5.0, nullable=False)

    user = relationship("User", back_populates="buyer_profile")


class DriverProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "driver_profiles"

    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    license_number = Column(String(50), nullable=True)
    rating = Column(Float, default=5.0, nullable=False)
    total_trips = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="driver_profile")
    vehicles = relationship("Vehicle", back_populates="driver", cascade="all, delete-orphan")


class Vehicle(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "vehicles"

    driver_id = Column(String(36), ForeignKey("driver_profiles.id"), nullable=False, index=True)
    vehicle_type = Column(String(50), nullable=False)  # Gazel, Isuzu, Kamaz, Ref, etc.
    plate_number = Column(String(30), nullable=False)
    capacity_tons = Column(Float, nullable=False)
    volume_m3 = Column(Float, nullable=True)
    is_refrigerated = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    driver = relationship("DriverProfile", back_populates="vehicles")
