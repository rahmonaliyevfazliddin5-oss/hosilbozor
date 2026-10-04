from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.i18n import t
from app.models.user import User, UserRole
from app.models.profile import DriverProfile, Vehicle
from app.models.order import Order
from app.models.logistics import DeliveryJob, DeliveryBid, JobStatus, BidStatus
from app.schemas.logistics import DeliveryJobCreate, DeliveryBidCreate
from app.repositories.logistics_repo import logistics_repo
from app.repositories.order_repo import order_repo


class LogisticsService:
    def create_job_for_order(
        self,
        db: Session,
        actor: User,
        payload: DeliveryJobCreate
    ) -> DeliveryJob:
        order = order_repo.get_by_id(db, payload.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")

        if actor.id not in (order.buyer_id, order.seller_id) and actor.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")

        # Fallback districts from listing if omitted
        pickup_district_id = payload.pickup_district_id
        if not pickup_district_id and order.listing:
            pickup_district_id = order.listing.district_id

        create_data = DeliveryJobCreate(
            order_id=order.id,
            proposed_price=payload.proposed_price or order.delivery_amount,
            pickup_district_id=pickup_district_id,
            delivery_district_id=payload.delivery_district_id
        )
        return logistics_repo.create_job(db, create_data)

    def submit_bid(
        self,
        db: Session,
        driver_user: User,
        job_id: str,
        payload: DeliveryBidCreate
    ) -> DeliveryBid:
        if driver_user.role != UserRole.DRIVER and driver_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Faqat haydovchilar taklif bera oladi")

        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == driver_user.id).first()
        if not driver_profile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Haydovchi profili topilmadi")

        # Verify vehicle belongs to driver
        vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id, Vehicle.driver_id == driver_profile.id).first()
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tanlangan transport vositasi sizga tegishli emas")

        job = logistics_repo.get_job_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yetkazib berish topshirig'i topilmadi")

        if job.status != JobStatus.OPEN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ushbu yuk allaqachon biriktirilgan yoki yakunlangan")

        return logistics_repo.create_bid(db, job_id=job.id, driver_id=driver_profile.id, payload=payload)

    def accept_bid(
        self,
        db: Session,
        actor: User,
        bid_id: str
    ) -> DeliveryJob:
        bid = logistics_repo.get_bid_by_id(db, bid_id)
        if not bid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Haydovchi taklifi topilmadi")

        job = bid.job
        order = job.order
        if order and actor.id not in (order.buyer_id, order.seller_id) and actor.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")

        if job.status != JobStatus.OPEN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topshiriq holati ochiq emas")

        return logistics_repo.accept_bid(db, job, bid)

    def start_trip(
        self,
        db: Session,
        driver_user: User,
        job_id: str,
        pickup_proof_url: Optional[str] = None
    ) -> DeliveryJob:
        job = logistics_repo.get_job_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topshiriq topilmadi")

        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == driver_user.id).first()
        if not driver_profile or job.driver_id != driver_profile.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Siz bu yukka biriktirilmagansiz")

        if job.status != JobStatus.ASSIGNED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topshiriq holati noto'g'ri")

        return logistics_repo.update_job_status(db, job, JobStatus.IN_TRANSIT, proof_url=pickup_proof_url)

    def complete_trip(
        self,
        db: Session,
        driver_user: User,
        job_id: str,
        delivery_proof_url: Optional[str] = None
    ) -> DeliveryJob:
        job = logistics_repo.get_job_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topshiriq topilmadi")

        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == driver_user.id).first()
        if not driver_profile or job.driver_id != driver_profile.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Siz bu yukka biriktirilmagansiz")

        if job.status != JobStatus.IN_TRANSIT:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yuk yo'lda (IN_TRANSIT) holatida emas")

        # Increment driver completed trips
        driver_profile.total_trips += 1
        db.commit()

        return logistics_repo.update_job_status(db, job, JobStatus.DELIVERED, proof_url=delivery_proof_url)


logistics_service = LogisticsService()
