import io
from decimal import Decimal
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District
from app.models.listing import ListingStatus


def create_sample_taxonomy(db: Session):
    region = Region(code="tashkent_v", name_uz="Toshkent viloyati", name_ru="Ташкентская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Yangiyo'l tumani", name_ru="Янгиюльский район")
    db.add(district)

    crop = Crop(slug="pomidor", name_uz="Pomidor", name_ru="Помидоры", category="vegetables", standard_unit="kg")
    db.add(crop)
    db.commit()
    db.refresh(district)
    db.refresh(crop)
    return district, crop


def test_create_listing_farmer_success(client: TestClient, db: Session, farmer_headers: dict):
    district, crop = create_sample_taxonomy(db)

    payload = {
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 1500.0,
        "min_order_quantity": 100.0,
        "price_per_unit": 6500.0,
        "quality_grade": "premium",
        "latitude": 41.2995,
        "longitude": 69.2401,
        "description": "Yangi uzilgan shirin pomidorlar"
    }

    response = client.post("/api/v1/listings", headers=farmer_headers, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["crop_id"] == crop.id
    assert float(data["price_per_unit"]) == 6500.0
    assert data["status"] == "active"
    assert data["farmer"]["full_name"] == "Alisher Dehqon"


def test_create_listing_buyer_forbidden(client: TestClient, db: Session, buyer_headers: dict):
    district, crop = create_sample_taxonomy(db)

    payload = {
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 500.0,
        "price_per_unit": 5000.0
    }
    response = client.post("/api/v1/listings", headers=buyer_headers, json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_and_filter_listings(client: TestClient, db: Session, farmer_headers: dict):
    district, crop = create_sample_taxonomy(db)

    # Create 2 listings
    client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 2000.0,
        "price_per_unit": 5000.0,
        "quality_grade": "standard"
    })
    client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 500.0,
        "price_per_unit": 8000.0,
        "quality_grade": "premium"
    })

    # Filter by price <= 6000
    res_filtered = client.get(f"/api/v1/listings?max_price=6000&crop_id={crop.id}")
    assert res_filtered.status_code == status.HTTP_200_OK
    data = res_filtered.json()
    assert data["total"] == 1
    assert float(data["items"][0]["price_per_unit"]) == 5000.0


def test_spatial_nearby_search(client: TestClient, db: Session, farmer_headers: dict):
    district, crop = create_sample_taxonomy(db)

    # Listing 1: Tashkent center (lat: 41.2995, lon: 69.2401)
    client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "quantity": 1000.0,
        "price_per_unit": 6000.0,
        "latitude": 41.2995,
        "longitude": 69.2401
    })

    # Listing 2: Samarkand center (lat: 39.6542, lon: 66.9597) ~270km away
    client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "quantity": 3000.0,
        "price_per_unit": 5500.0,
        "latitude": 39.6542,
        "longitude": 66.9597
    })

    # Search within 25km radius around Tashkent center
    res_near = client.get("/api/v1/listings/nearby?latitude=41.3111&longitude=69.2797&radius_km=25")
    assert res_near.status_code == status.HTTP_200_OK
    items = res_near.json()
    assert len(items) == 1
    assert items[0]["distance_km"] < 25.0

    # Search within 350km radius
    res_wide = client.get("/api/v1/listings/nearby?latitude=41.3111&longitude=69.2797&radius_km=350")
    assert res_wide.status_code == status.HTTP_200_OK
    wide_items = res_wide.json()
    assert len(wide_items) == 2
    # Verify nearest comes first
    assert wide_items[0]["distance_km"] < wide_items[1]["distance_km"]


def test_listing_status_lifecycle_and_photo(client: TestClient, db: Session, farmer_headers: dict):
    district, crop = create_sample_taxonomy(db)

    # 1. Create listing
    create_resp = client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "quantity": 800.0,
        "price_per_unit": 7000.0
    })
    listing_id = create_resp.json()["id"]

    # 2. Upload photo (valid jpg)
    dummy_image = io.BytesIO(b"fake-image-content-for-testing")
    photo_resp = client.post(
        f"/api/v1/listings/{listing_id}/photos",
        headers=farmer_headers,
        files={"file": ("pomidor.jpg", dummy_image, "image/jpeg")},
        data={"is_cover": "true"}
    )
    assert photo_resp.status_code == status.HTTP_201_CREATED
    photo_data = photo_resp.json()
    assert photo_data["is_cover"] is True

    # 3. Transition status to reserved
    patch_resp = client.patch(
        f"/api/v1/listings/{listing_id}/status?status=reserved",
        headers=farmer_headers
    )
    assert patch_resp.status_code == status.HTTP_200_OK
    assert patch_resp.json()["status"] == "reserved"

    # 4. Delete photo
    del_photo = client.delete(
        f"/api/v1/listings/{listing_id}/photos/{photo_data['id']}",
        headers=farmer_headers
    )
    assert del_photo.status_code == status.HTTP_200_OK

    # 5. Delete listing
    del_resp = client.delete(f"/api/v1/listings/{listing_id}", headers=farmer_headers)
    assert del_resp.status_code == status.HTTP_200_OK
