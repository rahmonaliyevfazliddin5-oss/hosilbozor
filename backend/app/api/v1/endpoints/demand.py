from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.demand import DemandStatus
from app.schemas.demand import (
    DemandRequestCreate,
    DemandRequestRead,
    DemandListResponse,
    OfferCreate,
    OfferRead,
    BuyerSummaryInDemand,
    FarmerSummaryInOffer
)
from app.schemas.order import OrderRead
from app.repositories.demand_repo import demand_repo
from app.services.demand_service import demand_service

router = APIRouter()


def enrich_demand_read(demand) -> DemandRequestRead:
    buyer_summary = None
    if demand.buyer:
        buyer_summary = BuyerSummaryInDemand(
            id=demand.buyer.id,
            full_name=demand.buyer.full_name,
            phone=demand.buyer.phone,
            company_name=demand.buyer.buyer_profile.company_name if demand.buyer.buyer_profile else None
        )
    offers = []
    for off in demand.offers:
        farmer_summary = None
        if off.farmer:
            farmer_summary = FarmerSummaryInOffer(
                id=off.farmer.id,
                full_name=off.farmer.full_name,
                phone=off.farmer.phone,
                rating=off.farmer.farmer_profile.rating if off.farmer.farmer_profile else 5.0
            )
        offer_read = OfferRead.model_validate(off)
        offer_read.farmer = farmer_summary
        offers.append(offer_read)

    read_item = DemandRequestRead.model_validate(demand)
    read_item.buyer = buyer_summary
    read_item.offers_count = len(demand.offers)
    read_item.offers = offers
    return read_item


@router.post("", response_model=DemandRequestRead, status_code=status.HTTP_201_CREATED)
def create_demand(
    payload: DemandRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a reverse auction purchasing demand (Buyer only)."""
    demand = demand_service.create_demand(db, current_user, payload)
    return enrich_demand_read(demand)


@router.get("", response_model=DemandListResponse)
def list_demands(
    crop_id: Optional[str] = Query(None),
    destination_district_id: Optional[str] = Query(None),
    status: Optional[DemandStatus] = Query(DemandStatus.ACTIVE),
    buyer_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lists purchasing demands with status and crop filters."""
    total, items = demand_repo.list_demands(
        db,
        crop_id=crop_id,
        destination_district_id=destination_district_id,
        status=status,
        buyer_id=buyer_id,
        skip=skip,
        limit=limit
    )
    return DemandListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[enrich_demand_read(item) for item in items]
    )


@router.get("/{id}", response_model=DemandRequestRead)
def get_demand(id: str, db: Session = Depends(get_db)):
    """Retrieves demand details along with competing farmer bids."""
    demand = demand_repo.get_demand_by_id(db, id)
    if not demand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talabnoma topilmadi")
    return enrich_demand_read(demand)


@router.post("/{id}/offers", response_model=OfferRead, status_code=status.HTTP_201_CREATED)
def submit_offer(
    id: str,
    payload: OfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Farmer submits a competitive price/quantity offer for a demand request."""
    offer = demand_service.submit_offer(db, current_user, id, payload)
    farmer_summary = FarmerSummaryInOffer(
        id=current_user.id,
        full_name=current_user.full_name,
        phone=current_user.phone
    )
    read_item = OfferRead.model_validate(offer)
    read_item.farmer = farmer_summary
    return read_item


@router.post("/offers/{offer_id}/accept", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def accept_offer(
    offer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buyer accepts a specific offer, spawning an Order in CREATED status."""
    return demand_service.accept_offer(db, current_user, offer_id)
