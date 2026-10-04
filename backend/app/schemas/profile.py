from typing import Optional, List
from pydantic import BaseModel


class FarmerProfileUpdate(BaseModel):
    farm_name: Optional[str] = None
    region_id: Optional[str] = None
    district_id: Optional[str] = None


class FarmerProfileRead(FarmerProfileUpdate):
    id: str
    user_id: str
    rating: float
    total_deals: int

    class Config:
        from_attributes = True


class BuyerProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    buyer_type: Optional[str] = None


class BuyerProfileRead(BuyerProfileUpdate):
    id: str
    user_id: str
    rating: float

    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    vehicle_type: str
    plate_number: str
    capacity_tons: float
    volume_m3: Optional[float] = None
    is_refrigerated: bool = False


class VehicleRead(VehicleCreate):
    id: str
    driver_id: str
    is_active: bool

    class Config:
        from_attributes = True


class DriverProfileUpdate(BaseModel):
    license_number: Optional[str] = None
    is_available: Optional[bool] = None


class DriverProfileRead(DriverProfileUpdate):
    id: str
    user_id: str
    rating: float
    total_trips: int
    is_available: bool
    vehicles: List[VehicleRead] = []

    class Config:
        from_attributes = True
