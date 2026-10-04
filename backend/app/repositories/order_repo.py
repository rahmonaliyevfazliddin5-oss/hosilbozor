import random
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.models.order import Order, OrderEvent, OrderStatus
from app.models.listing import Listing, ListingStatus


def generate_order_number() -> str:
    timestamp = datetime.now().strftime("%y%m%d")
    rand = f"{random.randint(1000, 9999)}"
    return f"HB-{timestamp}-{rand}"


def generate_verification_code() -> str:
    return f"{random.randint(100000, 999999)}"


class OrderRepository:
    def create_order(
        self,
        db: Session,
        buyer_id: str,
        seller_id: str,
        quantity: Decimal,
        price_per_unit: Decimal,
        delivery_amount: Decimal = Decimal("0.0"),
        platform_fee_percent: Decimal = Decimal("0.02"),  # 2% standard platform fee
        listing_id: Optional[str] = None,
        offer_id: Optional[str] = None
    ) -> Order:
        total_product_amount = quantity * price_per_unit
        platform_fee = (total_product_amount * platform_fee_percent).quantize(Decimal("1.0"))
        total_amount = total_product_amount + delivery_amount + platform_fee

        order = Order(
            order_number=generate_order_number(),
            buyer_id=buyer_id,
            seller_id=seller_id,
            listing_id=listing_id,
            offer_id=offer_id,
            quantity=quantity,
            price_per_unit=price_per_unit,
            total_product_amount=total_product_amount,
            delivery_amount=delivery_amount,
            platform_fee=platform_fee,
            total_amount=total_amount,
            status=OrderStatus.CREATED,
            pickup_code=generate_verification_code(),
            delivery_code=generate_verification_code()
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Record initial event
        self.record_event(
            db,
            order_id=order.id,
            from_status=None,
            to_status=OrderStatus.CREATED.value,
            user_id=buyer_id,
            notes="Buyurtma yaratildi"
        )
        return order

    def get_by_id(self, db: Session, order_id: str) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()

    def get_by_order_number(self, db: Session, order_number: str) -> Optional[Order]:
        return db.query(Order).filter(Order.order_number == order_number).first()

    def list_orders(
        self,
        db: Session,
        user_id: Optional[str] = None,
        status: Optional[OrderStatus] = None,
        role: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[Order]]:
        query = db.query(Order)

        if user_id:
            if role == "buyer":
                query = query.filter(Order.buyer_id == user_id)
            elif role == "seller" or role == "farmer":
                query = query.filter(Order.seller_id == user_id)
            else:
                query = query.filter(or_(Order.buyer_id == user_id, Order.seller_id == user_id))

        if status:
            query = query.filter(Order.status == status)

        query = query.order_by(desc(Order.created_at))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def record_event(
        self,
        db: Session,
        order_id: str,
        from_status: Optional[str],
        to_status: str,
        user_id: Optional[str],
        notes: Optional[str] = None
    ) -> OrderEvent:
        event = OrderEvent(
            order_id=order_id,
            from_status=from_status,
            to_status=to_status,
            triggered_by=user_id,
            notes=notes
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def set_status(
        self,
        db: Session,
        order: Order,
        new_status: OrderStatus,
        user_id: Optional[str],
        notes: Optional[str] = None
    ) -> Order:
        old_status = order.status.value
        order.status = new_status
        db.commit()
        db.refresh(order)
        self.record_event(
            db,
            order_id=order.id,
            from_status=old_status,
            to_status=new_status.value,
            user_id=user_id,
            notes=notes
        )
        return order


order_repo = OrderRepository()
