import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, List
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.i18n import t
from app.models.user import User, UserRole
from app.models.listing import Listing, ListingPhoto, ListingStatus
from app.schemas.listing import ListingCreate, ListingUpdate, ListingRead, FarmerSummary
from app.repositories.listing_repo import listing_repo

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class ListingService:
    def create_listing(self, db: Session, user: User, payload: ListingCreate) -> Listing:
        if user.role != UserRole.FARMER and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", user.language)
            )
        return listing_repo.create(db, farmer_id=user.id, payload=payload)

    def update_listing(self, db: Session, user: User, listing_id: str, payload: ListingUpdate) -> Listing:
        listing = listing_repo.get_by_id(db, listing_id)
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=t("listings.not_found", user.language)
            )
        if listing.farmer_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", user.language)
            )
        return listing_repo.update(db, listing, payload)

    def transition_status(self, db: Session, user: User, listing_id: str, new_status: ListingStatus) -> Listing:
        return self.update_listing(db, user, listing_id, ListingUpdate(status=new_status))

    def upload_photo(
        self,
        db: Session,
        user: User,
        listing_id: str,
        file: UploadFile,
        is_cover: bool = False
    ) -> ListingPhoto:
        listing = listing_repo.get_by_id(db, listing_id)
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=t("listings.not_found", user.language)
            )
        if listing.farmer_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("auth.forbidden", user.language)
            )

        # Validate extension
        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fayl formati yaroqsiz. Ruxsat berilgan: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Save to disk
        upload_dir = Path(settings.UPLOAD_DIR) / "listings" / listing_id
        upload_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}{ext}"
        target_path = upload_dir / filename

        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Relative public URL
        photo_url = f"/uploads/listings/{listing_id}/{filename}"
        return listing_repo.add_photo(db, listing_id=listing_id, photo_url=photo_url, is_cover=is_cover)

    def enrich_listing_read(self, listing: Listing, distance_km: Optional[float] = None) -> ListingRead:
        farmer_summary = None
        if listing.farmer:
            farm_name = (
                listing.farmer.farmer_profile.farm_name
                if listing.farmer.farmer_profile
                else None
            )
            rating = (
                listing.farmer.farmer_profile.rating
                if listing.farmer.farmer_profile
                else 5.0
            )
            farmer_summary = FarmerSummary(
                id=listing.farmer.id,
                full_name=listing.farmer.full_name,
                phone=listing.farmer.phone,
                farm_name=farm_name,
                rating=rating
            )

        read_item = ListingRead.model_validate(listing)
        read_item.farmer = farmer_summary
        read_item.distance_km = distance_km
        return read_item


listing_service = ListingService()
