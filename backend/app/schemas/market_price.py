from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.meta import CropRead, RegionRead


class MarketPriceCreate(BaseModel):
    crop_id: str
    region_id: str
    market_name: str
    min_price: Decimal = Field(..., gt=0)
    max_price: Decimal = Field(..., gt=0)
    avg_price: Decimal = Field(..., gt=0)
    recorded_date: date


class MarketPriceRead(MarketPriceCreate):
    id: str
    created_at: datetime
    crop: Optional[CropRead] = None
    region: Optional[RegionRead] = None

    class Config:
        from_attributes = True


class PriceHistoryPoint(BaseModel):
    recorded_date: date
    min_price: Decimal
    max_price: Decimal
    avg_price: Decimal
    market_name: str


class PriceHistoryResponse(BaseModel):
    crop_id: str
    region_id: Optional[str] = None
    crop_name: str
    history: List[PriceHistoryPoint]


class PriceAlertCreate(BaseModel):
    crop_id: str
    region_id: Optional[str] = None
    target_price: Decimal = Field(..., gt=0)
    condition: str = Field(default="below", pattern="^(below|above)$")


class PriceAlertRead(PriceAlertCreate):
    id: str
    user_id: str
    created_at: datetime
    crop: Optional[CropRead] = None

    class Config:
        from_attributes = True


class CSVImportResult(BaseModel):
    total_rows: int
    imported: int
    skipped: int
    errors: List[str] = []
