from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.i18n import t
from app.models.user import User, UserRole
from app.models.demand import DemandRequest, Offer, DemandStatus, OfferStatus
from app.models.order import Order
from app.schemas.demand import DemandRequestCreate, OfferCreate
from app.repositories.demand_repo import demand_repo
from app.repositories.order_repo import order_repo


class DemandService:
    def create_demand(self, db: Session, buyer: User, payload: DemandRequestCreate) -> DemandRequest:
        if buyer.role != UserRole.BUYER and buyer.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", buyer.language)
            )
        return demand_repo.create_demand(db, buyer_id=buyer.id, payload=payload)

    def submit_offer(self, db: Session, farmer: User, demand_id: str, payload: OfferCreate) -> Offer:
        if farmer.role != UserRole.FARMER and farmer.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", farmer.language)
            )

        demand = demand_repo.get_demand_by_id(db, demand_id)
        if not demand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Talabnomasi topilmadi"
            )
        if demand.status != DemandStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu talabnoma faol emas yoki yakunlangan"
            )

        return demand_repo.create_offer(db, demand_id=demand_id, farmer_id=farmer.id, payload=payload)

    def accept_offer(self, db: Session, buyer: User, offer_id: str) -> Order:
        offer = demand_repo.get_offer_id(db, offer_id) if hasattr(demand_repo, "get_offer_id") else demand_repo.get_offer_by_id(db, offer_id)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Taklif topilmadi"
            )

        demand = offer.demand
        if demand.buyer_id != buyer.id and buyer.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", buyer.language)
            )

        if demand.status != DemandStatus.ACTIVE or offer.status != OfferStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Taklifni qabul qilib bo'lmaydi (allaqachon qabul qilingan yoki bekor qilingan)"
            )

        # 1. Accept this offer
        demand_repo.update_offer_status(db, offer, OfferStatus.ACCEPTED)

        # 2. Reject other pending offers
        all_offers = demand_repo.list_offers_for_demand(db, demand.id)
        for other in all_offers:
            if other.id != offer.id and other.status == OfferStatus.PENDING:
                demand_repo.update_offer_status(db, other, OfferStatus.REJECTED)

        # 3. Mark demand fulfilled
        demand_repo.update_demand_status(db, demand, DemandStatus.FULFILLED)

        # 4. Create Order automatically from accepted reverse auction offer
        order = order_repo.create_order(
            db,
            buyer_id=demand.buyer_id,
            seller_id=offer.farmer_id,
            quantity=offer.offered_quantity,
            price_per_unit=offer.offered_price_per_unit,
            offer_id=offer.id
        )
        return order


demand_service = DemandService()
