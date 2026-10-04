from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User, UserRole
from app.models.logistics import JobStatus
from app.models.profile import DriverProfile
from app.schemas.logistics import (
    DeliveryJobCreate,
    DeliveryJobRead,
    DeliveryJobListResponse,
    DeliveryBidCreate,
    DeliveryBidRead,
    DriverSummaryInBid
)
from app.repositories.logistics_repo import logistics_repo
from app.services.logistics_service import logistics_service

router = APIRouter()


def enrich_job_read(job) -> DeliveryJobRead:
    bids_read = []
    for b in job.bids:
        driver_summary = None
        if b.driver and b.driver.user:
            driver_summary = DriverSummaryInBid(
                id=b.driver.id,
                user_id=b.driver.user_id,
                full_name=b.driver.user.full_name,
                phone=b.driver.user.phone,
                rating=b.driver.rating,
                total_trips=b.driver.total_trips
            )
        b_read = DeliveryBidRead.model_validate(b)
        b_read.driver = driver_summary
        bids_read.append(b_read)

    read_item = DeliveryJobRead.model_validate(job)
    read_item.bids = bids_read
    return read_item


@router.post("/jobs", response_model=DeliveryJobRead, status_code=status.HTTP_201_CREATED)
def create_delivery_job(
    payload: DeliveryJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a logistics job for a customer order."""
    job = logistics_service.create_job_for_order(db, current_user, payload)
    return enrich_job_read(job)


@router.get("/jobs", response_model=DeliveryJobListResponse)
def list_delivery_jobs(
    status: Optional[JobStatus] = Query(JobStatus.OPEN),
    pickup_district_id: Optional[str] = Query(None),
    delivery_district_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lists available cargo delivery jobs for truck drivers."""
    total, items = logistics_repo.list_jobs(
        db,
        status=status,
        pickup_district_id=pickup_district_id,
        delivery_district_id=delivery_district_id,
        skip=skip,
        limit=limit
    )
    return DeliveryJobListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[enrich_job_read(j) for j in items]
    )


@router.get("/jobs/{id}", response_model=DeliveryJobRead)
def get_delivery_job(id: str, db: Session = Depends(get_db)):
    """Retrieves delivery job details along with incoming bids."""
    job = logistics_repo.get_job_by_id(db, id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topshiriq topilmadi")
    return enrich_job_read(job)


@router.post("/jobs/{id}/bids", response_model=DeliveryBidRead, status_code=status.HTTP_201_CREATED)
def submit_delivery_bid(
    id: str,
    payload: DeliveryBidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.DRIVER]))
):
    """Driver places a delivery fee proposal for a cargo job."""
    bid = logistics_service.submit_bid(db, current_user, id, payload)
    driver_summary = DriverSummaryInBid(
        id=bid.driver.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        phone=current_user.phone,
        rating=bid.driver.rating,
        total_trips=bid.driver.total_trips
    )
    read_item = DeliveryBidRead.model_validate(bid)
    read_item.driver = driver_summary
    return read_item


@router.post("/bids/{bid_id}/accept", response_model=DeliveryJobRead)
def accept_delivery_bid(
    bid_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Customer/Farmer accepts driver's bid and assigns cargo to the driver."""
    job = logistics_service.accept_bid(db, current_user, bid_id)
    return enrich_job_read(job)


@router.post("/jobs/{id}/start", response_model=DeliveryJobRead)
def start_delivery_trip(
    id: str,
    proof_url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.DRIVER]))
):
    """Driver initiates transit after picking up goods."""
    job = logistics_service.start_trip(db, current_user, id, proof_url)
    return enrich_job_read(job)


@router.post("/jobs/{id}/deliver", response_model=DeliveryJobRead)
def complete_delivery_trip(
    id: str,
    proof_url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.DRIVER]))
):
    """Driver records cargo arrival with delivery proof."""
    job = logistics_service.complete_trip(db, current_user, id, proof_url)
    return enrich_job_read(job)


@router.get("/my-trips", response_model=DeliveryJobListResponse)
def list_my_driver_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.DRIVER]))
):
    """Lists current driver's assigned trips."""
    driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
    if not driver_profile:
        return DeliveryJobListResponse(total=0, skip=0, limit=20, items=[])

    total, items = logistics_repo.list_jobs(db, status=None, driver_id=driver_profile.id)
    return DeliveryJobListResponse(
        total=total,
        skip=0,
        limit=20,
        items=[enrich_job_read(j) for j in items]
    )
