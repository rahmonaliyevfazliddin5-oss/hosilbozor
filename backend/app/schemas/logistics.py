from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.logistics import JobStatus, BidStatus
from app.schemas.profile import VehicleRead, DriverProfileRead
from app.schemas.meta import DistrictRead


class DeliveryBidBase(BaseModel):
    bid_amount: Decimal = Field(..., gt=0, description="Proposed delivery fee in UZS")
    estimated_hours: Optional[int] = Field(None, gt=0)


class DeliveryBidCreate(DeliveryBidBase):
    vehicle_id: str


class DriverSummaryInBid(BaseModel):
    id: str
    user_id: str
    full_name: str = ""
    phone: Optional[str] = None
    rating: float = 5.0
    total_trips: int = 0

    class Config:
        from_attributes = True


class DeliveryBidRead(DeliveryBidBase):
    id: str
    job_id: str
    driver_id: str
    vehicle_id: str
    status: BidStatus
    created_at: datetime
    driver: Optional[DriverSummaryInBid] = None
    vehicle: Optional[VehicleRead] = None

    class Config:
        from_attributes = True


class DeliveryJobCreate(BaseModel):
    order_id: str
    proposed_price: Optional[Decimal] = Field(None, gt=0)
    pickup_district_id: Optional[str] = None
    delivery_district_id: Optional[str] = None


class DeliveryJobRead(BaseModel):
    id: str
    order_id: str
    driver_id: Optional[str] = None
    pickup_district_id: Optional[str] = None
    delivery_district_id: Optional[str] = None
    proposed_price: Optional[Decimal] = None
    agreed_price: Optional[Decimal] = None
    status: JobStatus
    pickup_proof_url: Optional[str] = None
    delivery_proof_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    pickup_district: Optional[DistrictRead] = None
    delivery_district: Optional[DistrictRead] = None
    driver: Optional[DriverProfileRead] = None
    bids: List[DeliveryBidRead] = []

    class Config:
        from_attributes = True


class DeliveryJobListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[DeliveryJobRead]
