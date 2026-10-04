from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.demand import DemandRequest, Offer, DemandStatus, OfferStatus
from app.schemas.demand import DemandRequestCreate, OfferCreate


class DemandRepository:
    def create_demand(self, db: Session, buyer_id: str, payload: DemandRequestCreate) -> DemandRequest:
        demand = DemandRequest(
            buyer_id=buyer_id,
            crop_id=payload.crop_id,
            destination_district_id=payload.destination_district_id,
            target_quantity=payload.target_quantity,
            max_price_per_unit=payload.max_price_per_unit,
            expires_at=payload.expires_at,
            description=payload.description,
            status=DemandStatus.ACTIVE
        )
        db.add(demand)
        db.commit()
        db.refresh(demand)
        return demand

    def get_demand_by_id(self, db: Session, demand_id: str) -> Optional[DemandRequest]:
        return db.query(DemandRequest).filter(DemandRequest.id == demand_id).first()

    def list_demands(
        self,
        db: Session,
        crop_id: Optional[str] = None,
        destination_district_id: Optional[str] = None,
        status: Optional[DemandStatus] = DemandStatus.ACTIVE,
        buyer_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[DemandRequest]]:
        query = db.query(DemandRequest)
        if status:
            query = query.filter(DemandRequest.status == status)
        if buyer_id:
            query = query.filter(DemandRequest.buyer_id == buyer_id)
        if crop_id:
            query = query.filter(DemandRequest.crop_id == crop_id)
        if destination_district_id:
            query = query.filter(DemandRequest.destination_district_id == destination_district_id)

        query = query.order_by(desc(DemandRequest.created_at))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def update_demand_status(self, db: Session, demand: DemandRequest, new_status: DemandStatus) -> DemandRequest:
        demand.status = new_status
        db.commit()
        db.refresh(demand)
        return demand

    def create_offer(self, db: Session, demand_id: str, farmer_id: str, payload: OfferCreate) -> Offer:
        offer = Offer(
            demand_id=demand_id,
            farmer_id=farmer_id,
            offered_price_per_unit=payload.offered_price_per_unit,
            offered_quantity=payload.offered_quantity,
            notes=payload.notes,
            status=OfferStatus.PENDING
        )
        db.add(offer)
        db.commit()
        db.refresh(offer)
        return offer

    def get_offer_by_id(self, db: Session, offer_id: str) -> Optional[Offer]:
        return db.query(Offer).filter(Offer.id == offer_id).first()

    def list_offers_for_demand(self, db: Session, demand_id: str) -> List[Offer]:
        return db.query(Offer).filter(Offer.demand_id == demand_id).order_by(Offer.offered_price_per_unit.asc()).all()

    def update_offer_status(self, db: Session, offer: Offer, new_status: OfferStatus) -> Offer:
        offer.status = new_status
        db.commit()
        db.refresh(offer)
        return offer


demand_repo = DemandRepository()
