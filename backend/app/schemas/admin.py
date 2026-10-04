from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.models.review import DisputeStatus
from app.schemas.user import UserRead


class PlatformMetricsResponse(BaseModel):
    total_gmv_uzs: Decimal
    total_orders: int
    completed_orders: int
    fill_rate_percent: float
    total_users: int
    active_farmers: int
    active_buyers: int
    active_drivers: int
    avg_price_spread_percent: float


class DisputeResolutionRequest(BaseModel):
    action: str  # "release_to_seller" or "refund_to_buyer"
    resolution_notes: str


class DisputeRead(BaseModel):
    id: str
    order_id: str
    raised_by: str
    reason: str
    evidence_urls: Optional[str] = None
    status: DisputeStatus
    resolution: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class VerificationQueueUser(BaseModel):
    id: str
    full_name: str
    phone: Optional[str] = None
    telegram_id: Optional[int] = None
    role: str
    created_at: str

    class Config:
        from_attributes = True
