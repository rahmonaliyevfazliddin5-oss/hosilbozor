from decimal import Decimal
from typing import List, Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.user import User, UserRole
from app.models.order import Order, OrderStatus
from app.models.review import Dispute, DisputeStatus
from app.models.market_price import MarketPrice


class AdminRepository:
    def get_platform_metrics(self, db: Session) -> Dict[str, Any]:
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        completed_orders = db.query(func.count(Order.id)).filter(Order.status == OrderStatus.COMPLETED).scalar() or 0
        fill_rate = (completed_orders / total_orders * 100.0) if total_orders > 0 else 0.0

        gmv_val = db.query(func.sum(Order.total_amount)).filter(Order.status == OrderStatus.COMPLETED).scalar()
        total_gmv = Decimal(str(gmv_val)) if gmv_val else Decimal("0.0")

        total_users = db.query(func.count(User.id)).scalar() or 0
        farmers_count = db.query(func.count(User.id)).filter(User.role == UserRole.FARMER).scalar() or 0
        buyers_count = db.query(func.count(User.id)).filter(User.role == UserRole.BUYER).scalar() or 0
        drivers_count = db.query(func.count(User.id)).filter(User.role == UserRole.DRIVER).scalar() or 0

        # Calculate average market price spread: ((max_price - min_price) / avg_price) * 100
        spreads = []
        recent_prices = db.query(MarketPrice).order_by(desc(MarketPrice.recorded_date)).limit(20).all()
        for p in recent_prices:
            if p.avg_price and p.avg_price > 0:
                spread = float((p.max_price - p.min_price) / p.avg_price * Decimal("100.0"))
                spreads.append(spread)
        avg_spread = round(sum(spreads) / len(spreads), 1) if spreads else 12.5

        return {
            "total_gmv_uzs": total_gmv,
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "fill_rate_percent": round(fill_rate, 1),
            "total_users": total_users,
            "active_farmers": farmers_count,
            "active_buyers": buyers_count,
            "active_drivers": drivers_count,
            "avg_price_spread_percent": avg_spread
        }

    def get_unverified_users(self, db: Session) -> List[User]:
        return db.query(User).filter(User.is_verified == False).order_by(desc(User.created_at)).all()

    def verify_user(self, db: Session, user_id: str) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True
            db.commit()
            db.refresh(user)
        return user

    def get_disputes(self, db: Session, status: Optional[DisputeStatus] = None) -> List[Dispute]:
        query = db.query(Dispute)
        if status:
            query = query.filter(Dispute.status == status)
        return query.order_by(desc(Dispute.created_at)).all()

    def resolve_dispute(
        self,
        db: Session,
        dispute_id: str,
        admin_id: str,
        action: str,
        notes: str
    ) -> Optional[Dispute]:
        dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
        if not dispute:
            return None

        if action == "release_to_seller":
            dispute.status = DisputeStatus.RESOLVED_RELEASE
        elif action == "refund_to_buyer":
            dispute.status = DisputeStatus.RESOLVED_REFUND
        else:
            dispute.status = DisputeStatus.CANCELLED

        dispute.resolved_by = admin_id
        dispute.resolution = notes
        db.commit()
        db.refresh(dispute)
        return dispute


admin_repo = AdminRepository()
