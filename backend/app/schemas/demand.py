from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.demand import DemandStatus, OfferStatus
from app.schemas.meta import CropRead, DistrictRead


class OfferBase(BaseModel):
    offered_price_per_unit: Decimal = Field(..., gt=0, description="Price per unit in UZS")
    offered_quantity: Decimal = Field(..., gt=0, description="Quantity offered in crop units")
    notes: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class FarmerSummaryInOffer(BaseModel):
    id: str
    full_name: str
    phone: Optional[str] = None
    rating: float = 5.0

    class Config:
        from_attributes = True


class OfferRead(OfferBase):
    id: str
    demand_id: str
    farmer_id: str
    status: OfferStatus
    created_at: datetime
    farmer: Optional[FarmerSummaryInOffer] = None

    class Config:
        from_attributes = True


class DemandRequestBase(BaseModel):
    crop_id: str
    destination_district_id: Optional[str] = None
    target_quantity: Decimal = Field(..., gt=0, description="Total quantity needed")
    max_price_per_unit: Decimal = Field(..., gt=0, description="Max acceptable price per unit in UZS")
    expires_at: Optional[datetime] = None
    description: Optional[str] = None


class DemandRequestCreate(DemandRequestBase):
    pass


class BuyerSummaryInDemand(BaseModel):
    id: str
    full_name: str
    phone: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True


class DemandRequestRead(DemandRequestBase):
    id: str
    buyer_id: str
    status: DemandStatus
    created_at: datetime
    crop: Optional[CropRead] = None
    destination_district: Optional[DistrictRead] = None
    buyer: Optional[BuyerSummaryInDemand] = None
    offers_count: int = 0
    offers: List[OfferRead] = []

    class Config:
        from_attributes = True


class DemandListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[DemandRequestRead]
