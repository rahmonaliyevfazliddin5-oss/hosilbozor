from decimal import Decimal
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.logistics import DeliveryJob, DeliveryBid, JobStatus, BidStatus
from app.models.profile import DriverProfile
from app.models.order import Order
from app.schemas.logistics import DeliveryJobCreate, DeliveryBidCreate


class LogisticsRepository:
    def create_job(self, db: Session, payload: DeliveryJobCreate) -> DeliveryJob:
        existing = db.query(DeliveryJob).filter(DeliveryJob.order_id == payload.order_id).first()
        if existing:
            return existing

        job = DeliveryJob(
            order_id=payload.order_id,
            proposed_price=payload.proposed_price,
            pickup_district_id=payload.pickup_district_id,
            delivery_district_id=payload.delivery_district_id,
            status=JobStatus.OPEN
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def get_job_by_id(self, db: Session, job_id: str) -> Optional[DeliveryJob]:
        return db.query(DeliveryJob).filter(DeliveryJob.id == job_id).first()

    def get_job_by_order_id(self, db: Session, order_id: str) -> Optional[DeliveryJob]:
        return db.query(DeliveryJob).filter(DeliveryJob.order_id == order_id).first()

    def list_jobs(
        self,
        db: Session,
        status: Optional[JobStatus] = JobStatus.OPEN,
        pickup_district_id: Optional[str] = None,
        delivery_district_id: Optional[str] = None,
        driver_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[DeliveryJob]]:
        query = db.query(DeliveryJob)
        if status:
            query = query.filter(DeliveryJob.status == status)
        if pickup_district_id:
            query = query.filter(DeliveryJob.pickup_district_id == pickup_district_id)
        if delivery_district_id:
            query = query.filter(DeliveryJob.delivery_district_id == delivery_district_id)
        if driver_id:
            query = query.filter(DeliveryJob.driver_id == driver_id)

        query = query.order_by(desc(DeliveryJob.created_at))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def create_bid(
        self,
        db: Session,
        job_id: str,
        driver_id: str,
        payload: DeliveryBidCreate
    ) -> DeliveryBid:
        bid = DeliveryBid(
            job_id=job_id,
            driver_id=driver_id,
            vehicle_id=payload.vehicle_id,
            bid_amount=payload.bid_amount,
            estimated_hours=payload.estimated_hours,
            status=BidStatus.PENDING
        )
        db.add(bid)
        db.commit()
        db.refresh(bid)
        return bid

    def get_bid_by_id(self, db: Session, bid_id: str) -> Optional[DeliveryBid]:
        return db.query(DeliveryBid).filter(DeliveryBid.id == bid_id).first()

    def list_bids_for_job(self, db: Session, job_id: str) -> List[DeliveryBid]:
        return db.query(DeliveryBid).filter(DeliveryBid.job_id == job_id).order_by(DeliveryBid.bid_amount.asc()).all()

    def accept_bid(self, db: Session, job: DeliveryJob, bid: DeliveryBid) -> DeliveryJob:
        # 1. Accept this bid
        bid.status = BidStatus.ACCEPTED

        # 2. Reject other bids
        all_bids = self.list_bids_for_job(db, job.id)
        for other in all_bids:
            if other.id != bid.id and other.status == BidStatus.PENDING:
                other.status = BidStatus.REJECTED

        # 3. Assign driver to job
        job.driver_id = bid.driver_id
        job.agreed_price = bid.bid_amount
        job.status = JobStatus.ASSIGNED

        # 4. Synchronize Order delivery amount
        order = job.order
        if order:
            order.delivery_amount = bid.bid_amount
            order.total_amount = order.total_product_amount + order.delivery_amount + order.platform_fee

        db.commit()
        db.refresh(job)
        return job

    def update_job_status(
        self,
        db: Session,
        job: DeliveryJob,
        new_status: JobStatus,
        proof_url: Optional[str] = None
    ) -> DeliveryJob:
        job.status = new_status
        if proof_url:
            if new_status == JobStatus.IN_TRANSIT:
                job.pickup_proof_url = proof_url
            elif new_status == JobStatus.DELIVERED:
                job.delivery_proof_url = proof_url
        db.commit()
        db.refresh(job)
        return job


logistics_repo = LogisticsRepository()
