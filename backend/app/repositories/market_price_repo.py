from datetime import date, timedelta
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.market_price import MarketPrice, PriceAlert
from app.models.crop import Crop
from app.schemas.market_price import MarketPriceCreate, PriceAlertCreate


class MarketPriceRepository:
    def record_price(self, db: Session, payload: MarketPriceCreate) -> MarketPrice:
        # Check if record for same crop, region, market, and date already exists
        existing = db.query(MarketPrice).filter(
            MarketPrice.crop_id == payload.crop_id,
            MarketPrice.region_id == payload.region_id,
            MarketPrice.market_name == payload.market_name,
            MarketPrice.recorded_date == payload.recorded_date
        ).first()

        if existing:
            existing.min_price = payload.min_price
            existing.max_price = payload.max_price
            existing.avg_price = payload.avg_price
            db.commit()
            db.refresh(existing)
            return existing

        price_entry = MarketPrice(
            crop_id=payload.crop_id,
            region_id=payload.region_id,
            market_name=payload.market_name,
            min_price=payload.min_price,
            max_price=payload.max_price,
            avg_price=payload.avg_price,
            recorded_date=payload.recorded_date
        )
        db.add(price_entry)
        db.commit()
        db.refresh(price_entry)
        return price_entry

    def get_latest_daily_prices(
        self,
        db: Session,
        region_id: Optional[str] = None,
        crop_id: Optional[str] = None,
        target_date: Optional[date] = None
    ) -> List[MarketPrice]:
        query = db.query(MarketPrice)
        if target_date:
            query = query.filter(MarketPrice.recorded_date == target_date)
        else:
            # Subquery to pick latest date
            latest_date = db.query(func.max(MarketPrice.recorded_date)).scalar()
            if latest_date:
                query = query.filter(MarketPrice.recorded_date == latest_date)

        if region_id:
            query = query.filter(MarketPrice.region_id == region_id)
        if crop_id:
            query = query.filter(MarketPrice.crop_id == crop_id)

        return query.order_by(desc(MarketPrice.recorded_date), MarketPrice.market_name).all()

    def get_price_history(
        self,
        db: Session,
        crop_id: str,
        region_id: Optional[str] = None,
        days: int = 30
    ) -> List[MarketPrice]:
        since_date = date.today() - timedelta(days=days)
        query = db.query(MarketPrice).filter(
            MarketPrice.crop_id == crop_id,
            MarketPrice.recorded_date >= since_date
        )
        if region_id:
            query = query.filter(MarketPrice.region_id == region_id)

        return query.order_by(MarketPrice.recorded_date.asc()).all()

    def create_price_alert(self, db: Session, user_id: str, payload: PriceAlertCreate) -> PriceAlert:
        alert = PriceAlert(
            user_id=user_id,
            crop_id=payload.crop_id,
            region_id=payload.region_id,
            target_price=payload.target_price,
            condition=payload.condition
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    def list_user_alerts(self, db: Session, user_id: str) -> List[PriceAlert]:
        return db.query(PriceAlert).filter(PriceAlert.user_id == user_id).all()

    def delete_price_alert(self, db: Session, user_id: str, alert_id: str) -> bool:
        alert = db.query(PriceAlert).filter(PriceAlert.id == alert_id, PriceAlert.user_id == user_id).first()
        if alert:
            db.delete(alert)
            db.commit()
            return True
        return False


market_price_repo = MarketPriceRepository()
