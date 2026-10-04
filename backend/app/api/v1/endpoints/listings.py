from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User, UserRole
from app.models.listing import ListingStatus
from app.schemas.listing import (
    ListingCreate,
    ListingUpdate,
    ListingRead,
    ListingListResponse,
    ListingPhotoRead
)
from app.repositories.listing_repo import listing_repo
from app.services.listing_service import listing_service

router = APIRouter()


@router.post("", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def create_listing(
    payload: ListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new harvest listing (Farmer or Admin only)."""
    listing = listing_service.create_listing(db, current_user, payload)
    return listing_service.enrich_listing_read(listing)


@router.get("", response_model=ListingListResponse)
def list_listings(
    crop_id: Optional[str] = Query(None),
    region_id: Optional[str] = Query(None),
    district_id: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None),
    max_price: Optional[Decimal] = Query(None),
    min_quantity: Optional[Decimal] = Query(None),
    quality_grade: Optional[str] = Query(None),
    status: Optional[ListingStatus] = Query(ListingStatus.ACTIVE),
    farmer_id: Optional[str] = Query(None),
    sort_by: str = Query("freshness", pattern="^(freshness|price_asc|price_desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieves paginated listings matching filters with sorting."""
    total, items = listing_repo.list_filtered(
        db,
        crop_id=crop_id,
        region_id=region_id,
        district_id=district_id,
        min_price=min_price,
        max_price=max_price,
        min_qty=min_quantity,
        quality_grade=quality_grade,
        status=status,
        farmer_id=farmer_id,
        sort_by=sort_by,
        skip=skip,
        limit=limit
    )
    enriched_items = [listing_service.enrich_listing_read(item) for item in items]
    return ListingListResponse(total=total, skip=skip, limit=limit, items=enriched_items)


@router.get("/nearby", response_model=List[ListingRead])
def list_nearby_listings(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(50.0, gt=0, le=1000),
    crop_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Performs spatial proximity search, returning active listings within radius sorted by distance."""
    nearby_items = listing_repo.list_nearby(
        db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        crop_id=crop_id,
        skip=skip,
        limit=limit
    )
    return [listing_service.enrich_listing_read(item, dist) for item, dist in nearby_items]


@router.get("/{id}", response_model=ListingRead)
def get_listing(id: str, db: Session = Depends(get_db)):
    """Retrieves single listing by ID with full farmer and photo details."""
    listing = listing_repo.get_by_id(db, id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E'lon topilmadi")
    return listing_service.enrich_listing_read(listing)


@router.put("/{id}", response_model=ListingRead)
def update_listing(
    id: str,
    payload: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates listing fields (Owner or Admin only)."""
    listing = listing_service.update_listing(db, current_user, id, payload)
    return listing_service.enrich_listing_read(listing)


@router.patch("/{id}/status", response_model=ListingRead)
def update_listing_status(
    id: str,
    status: ListingStatus = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transitions listing status (e.g. draft, active, reserved, sold)."""
    listing = listing_service.transition_status(db, current_user, id, status)
    return listing_service.enrich_listing_read(listing)


@router.post("/{id}/photos", response_model=ListingPhotoRead, status_code=status.HTTP_201_CREATED)
def upload_listing_photo(
    id: str,
    file: UploadFile = File(...),
    is_cover: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Uploads and associates a photo artifact with the harvest listing."""
    return listing_service.upload_photo(db, current_user, id, file, is_cover)


@router.delete("/{id}/photos/{photo_id}", status_code=status.HTTP_200_OK)
def delete_listing_photo(
    id: str,
    photo_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes photo associated with listing."""
    listing = listing_repo.get_by_id(db, id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E'lon topilmadi")
    if listing.farmer_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")
    success = listing_repo.delete_photo(db, photo_id)
    return {"success": success}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_listing(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes listing (Owner or Admin only)."""
    listing = listing_repo.get_by_id(db, id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E'lon topilmadi")
    if listing.farmer_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat berilmagan")
    listing_repo.delete(db, listing)
    return {"success": True, "message": "E'lon o'chirildi"}
