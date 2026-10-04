from typing import Optional, List, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.models.listing import Listing, ListingPhoto, ListingStatus
from app.models.region import District
from app.schemas.listing import ListingCreate, ListingUpdate
from app.core.geo import calculate_haversine_distance


class ListingRepository:
    def create(self, db: Session, farmer_id: str, payload: ListingCreate) -> Listing:
        data = payload.model_dump()
        listing = Listing(
            farmer_id=farmer_id,
            crop_id=data["crop_id"],
            district_id=data.get("district_id"),
            quantity=data["quantity"],
            min_order_quantity=data.get("min_order_quantity", Decimal("1.0")),
            price_per_unit=data["price_per_unit"],
            quality_grade=data.get("quality_grade", "standard"),
            harvest_date=data.get("harvest_date"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            description=data.get("description"),
            status=ListingStatus.ACTIVE
        )
        db.add(listing)
        db.commit()
        db.refresh(listing)
        return listing

    def get_by_id(self, db: Session, listing_id: str) -> Optional[Listing]:
        return db.query(Listing).filter(Listing.id == listing_id).first()

    def update(self, db: Session, listing: Listing, payload: ListingUpdate) -> Listing:
        update_dict = payload.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(listing, key, value)
        db.commit()
        db.refresh(listing)
        return listing

    def delete(self, db: Session, listing: Listing) -> None:
        db.delete(listing)
        db.commit()

    def list_filtered(
        self,
        db: Session,
        crop_id: Optional[str] = None,
        region_id: Optional[str] = None,
        district_id: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        min_qty: Optional[Decimal] = None,
        quality_grade: Optional[str] = None,
        status: Optional[ListingStatus] = ListingStatus.ACTIVE,
        farmer_id: Optional[str] = None,
        sort_by: str = "freshness",
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[Listing]]:
        query = db.query(Listing)

        if status:
            query = query.filter(Listing.status == status)
        if farmer_id:
            query = query.filter(Listing.farmer_id == farmer_id)
        if crop_id:
            query = query.filter(Listing.crop_id == crop_id)
        if district_id:
            query = query.filter(Listing.district_id == district_id)
        elif region_id:
            query = query.join(District, Listing.district_id == District.id).filter(District.region_id == region_id)
        if min_price is not None:
            query = query.filter(Listing.price_per_unit >= min_price)
        if max_price is not None:
            query = query.filter(Listing.price_per_unit <= max_price)
        if min_qty is not None:
            query = query.filter(Listing.quantity >= min_qty)
        if quality_grade:
            query = query.filter(Listing.quality_grade == quality_grade)

        # Sorting
        if sort_by == "price_asc":
            query = query.order_by(asc(Listing.price_per_unit))
        elif sort_by == "price_desc":
            query = query.order_by(desc(Listing.price_per_unit))
        else:  # "freshness"
            query = query.order_by(desc(Listing.created_at))

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def list_nearby(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float = 50.0,
        crop_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Tuple[Listing, float]]:
        """
        Retrieves active listings within the specified radius (in km),
        computing distance and sorting by nearest first.
        """
        query = db.query(Listing).filter(
            Listing.status == ListingStatus.ACTIVE,
            Listing.latitude.isnot(None),
            Listing.longitude.isnot(None)
        )
        if crop_id:
            query = query.filter(Listing.crop_id == crop_id)

        all_active = query.all()
        nearby_results = []

        for item in all_active:
            dist = calculate_haversine_distance(latitude, longitude, item.latitude, item.longitude)
            if dist is not None and dist <= radius_km:
                nearby_results.append((item, dist))

        # Sort by distance ascending
        nearby_results.sort(key=lambda x: x[1])
        return nearby_results[skip : skip + limit]

    def add_photo(
        self,
        db: Session,
        listing_id: str,
        photo_url: str,
        is_cover: bool = False,
        sort_order: int = 0
    ) -> ListingPhoto:
        if is_cover:
            # Unset existing covers
            db.query(ListingPhoto).filter(ListingPhoto.listing_id == listing_id).update({"is_cover": False})

        photo = ListingPhoto(
            listing_id=listing_id,
            photo_url=photo_url,
            is_cover=is_cover,
            sort_order=sort_order
        )
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo

    def delete_photo(self, db: Session, photo_id: str) -> bool:
        photo = db.query(ListingPhoto).filter(ListingPhoto.id == photo_id).first()
        if photo:
            db.delete(photo)
            db.commit()
            return True
        return False


listing_repo = ListingRepository()
