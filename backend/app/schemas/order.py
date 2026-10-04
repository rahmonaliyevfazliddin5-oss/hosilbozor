from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.order import OrderStatus
from app.schemas.listing import ListingRead
from app.schemas.demand import OfferRead


class UserSummaryInOrder(BaseModel):
    id: str
    full_name: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class OrderEventRead(BaseModel):
    id: str
    from_status: Optional[str] = None
    to_status: str
    triggered_by: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreateFromListing(BaseModel):
    listing_id: str
    quantity: Decimal = Field(..., gt=0, description="Quantity to order")
    delivery_amount: Decimal = Field(default=Decimal("0.0"), ge=0)


class OrderPickupVerificationRequest(BaseModel):
    pickup_code: str = Field(..., min_length=4, max_length=10)


class OrderDeliveryVerificationRequest(BaseModel):
    delivery_code: str = Field(..., min_length=4, max_length=10)
    proof_photo_url: Optional[str] = None


class OrderDisputeRequest(BaseModel):
    reason: str = Field(..., min_length=10)
    evidence_urls: Optional[str] = None


class OrderRead(BaseModel):
    id: str
    order_number: str
    buyer_id: str
    seller_id: str
    listing_id: Optional[str] = None
    offer_id: Optional[str] = None
    quantity: Decimal
    price_per_unit: Decimal
    total_product_amount: Decimal
    delivery_amount: Decimal
    platform_fee: Decimal
    total_amount: Decimal
    status: OrderStatus
    pickup_code: Optional[str] = None
    delivery_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    buyer: Optional[UserSummaryInOrder] = None
    seller: Optional[UserSummaryInOrder] = None
    listing: Optional[ListingRead] = None
    events: List[OrderEventRead] = []

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[OrderRead]
