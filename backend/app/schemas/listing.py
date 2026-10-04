from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.listing import ListingStatus
from app.schemas.meta import CropRead, DistrictRead


class ListingPhotoCreate(BaseModel):
    photo_url: str
    is_cover: bool = False
    sort_order: int = 0


class ListingPhotoRead(ListingPhotoCreate):
    id: str
    listing_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ListingBase(BaseModel):
    crop_id: str
    district_id: Optional[str] = None
    quantity: Decimal = Field(..., gt=0, description="Available quantity in crop units")
    min_order_quantity: Decimal = Field(default=Decimal("1.0"), gt=0)
    price_per_unit: Decimal = Field(..., gt=0, description="Price per unit in UZS")
    quality_grade: str = Field(default="standard", description="premium, standard, or processing")
    harvest_date: Optional[date] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    quantity: Optional[Decimal] = Field(None, gt=0)
    min_order_quantity: Optional[Decimal] = Field(None, gt=0)
    price_per_unit: Optional[Decimal] = Field(None, gt=0)
    quality_grade: Optional[str] = None
    harvest_date: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    status: Optional[ListingStatus] = None


class FarmerSummary(BaseModel):
    id: str
    full_name: str
    phone: Optional[str] = None
    farm_name: Optional[str] = None
    rating: float = 5.0

    class Config:
        from_attributes = True


class ListingRead(ListingBase):
    id: str
    farmer_id: str
    status: ListingStatus
    created_at: datetime
    updated_at: datetime
    crop: Optional[CropRead] = None
    district: Optional[DistrictRead] = None
    photos: List[ListingPhotoRead] = []
    farmer: Optional[FarmerSummary] = None
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True


class ListingListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ListingRead]
