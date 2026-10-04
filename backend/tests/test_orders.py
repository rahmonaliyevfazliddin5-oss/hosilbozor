from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District
from app.models.order import Order


def setup_order_prerequisites(client: TestClient, db: Session, farmer_headers: dict):
    region = Region(code="fergana", name_uz="Farg'ona viloyati", name_ru="Ферганская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Quva tumani", name_ru="Кувинский район")
    db.add(district)

    crop = Crop(slug="anor", name_uz="Anor", name_ru="Гранат", category="fruits", standard_unit="kg")
    db.add(crop)
    db.commit()
    db.refresh(district)
    db.refresh(crop)

    # Farmer creates listing: 5000 kg anor @ 15,000 UZS
    listing_resp = client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 5000.0,
        "min_order_quantity": 500.0,
        "price_per_unit": 15000.0
    })
    return listing_resp.json()


def test_order_happy_path_state_machine(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    listing_data = setup_order_prerequisites(client, db, farmer_headers)
    listing_id = listing_data["id"]

    # 1. Buyer creates order for 1,000 kg
    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 1000.0,
        "delivery_amount": 500000.0
    })
    assert order_resp.status_code == status.HTTP_201_CREATED
    order_data = order_resp.json()
    order_id = order_data["id"]
    assert order_data["status"] == "created"
    assert float(order_data["total_product_amount"]) == 15000000.0

    # 2. Farmer confirms order
    confirm_resp = client.post(f"/api/v1/orders/{order_id}/confirm", headers=farmer_headers)
    assert confirm_resp.status_code == status.HTTP_200_OK
    assert confirm_resp.json()["status"] == "confirmed"

    # 3. Buyer locks funds in escrow
    pay_resp = client.post(f"/api/v1/orders/{order_id}/pay-escrow", headers=buyer_headers)
    assert pay_resp.status_code == status.HTTP_200_OK
    assert pay_resp.json()["status"] == "paid_escrow"

    # Fetch fresh order from DB to get the secret pickup and delivery codes
    order_obj = db.query(Order).filter(Order.id == order_id).first()
    pickup_code = order_obj.pickup_code
    delivery_code = order_obj.delivery_code

    # 4. Wrong pickup code fails
    bad_pickup = client.post(f"/api/v1/orders/{order_id}/verify-pickup", headers=farmer_headers, json={
        "pickup_code": "000000"
    })
    assert bad_pickup.status_code == status.HTTP_400_BAD_REQUEST

    # 5. Valid pickup code transitions to PICKED_UP
    pickup_resp = client.post(f"/api/v1/orders/{order_id}/verify-pickup", headers=farmer_headers, json={
        "pickup_code": pickup_code
    })
    assert pickup_resp.status_code == status.HTTP_200_OK
    assert pickup_resp.json()["status"] == "picked_up"

    # 6. Wrong delivery code fails
    bad_del = client.post(f"/api/v1/orders/{order_id}/verify-delivery", headers=buyer_headers, json={
        "delivery_code": "111111"
    })
    assert bad_del.status_code == status.HTTP_400_BAD_REQUEST

    # 7. Valid delivery code transitions to DELIVERED
    del_resp = client.post(f"/api/v1/orders/{order_id}/verify-delivery", headers=buyer_headers, json={
        "delivery_code": delivery_code,
        "proof_photo_url": "https://cdn.hosilbozor.uz/proof/delivery-1.jpg"
    })
    assert del_resp.status_code == status.HTTP_200_OK
    assert del_resp.json()["status"] == "delivered"

    # 8. Buyer confirms completion -> COMPLETED
    comp_resp = client.post(f"/api/v1/orders/{order_id}/complete", headers=buyer_headers)
    assert comp_resp.status_code == status.HTTP_200_OK
    assert comp_resp.json()["status"] == "completed"

    # 9. Verify event audit logs contain all lifecycle states
    order_detail = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    event_statuses = [ev["to_status"] for ev in order_detail["events"]]
    assert "created" in event_statuses
    assert "confirmed" in event_statuses
    assert "paid_escrow" in event_statuses
    assert "picked_up" in event_statuses
    assert "delivered" in event_statuses
    assert "completed" in event_statuses


def test_invalid_state_transition_rejected(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    listing_data = setup_order_prerequisites(client, db, farmer_headers)
    listing_id = listing_data["id"]

    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 500.0
    })
    order_id = order_resp.json()["id"]

    # Attempting to directly complete an order that is only in 'created' status must fail!
    invalid_jump = client.post(f"/api/v1/orders/{order_id}/complete", headers=buyer_headers)
    assert invalid_jump.status_code == status.HTTP_400_BAD_REQUEST
    assert "Noto'g'ri holat o'tishi" in invalid_jump.json()["detail"]


def test_order_cancellation_restores_listing(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    listing_data = setup_order_prerequisites(client, db, farmer_headers)
    listing_id = listing_data["id"]

    # Initial quantity is 5000.0
    # Order 5000.0 (entire quantity)
    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 5000.0
    })
    order_id = order_resp.json()["id"]

    # Check listing is reserved/0 quantity
    listing_check = client.get(f"/api/v1/listings/{listing_id}").json()
    assert float(listing_check["quantity"]) == 0.0

    # Cancel order
    cancel_resp = client.post(f"/api/v1/orders/{order_id}/cancel", headers=buyer_headers)
    assert cancel_resp.status_code == status.HTTP_200_OK
    assert cancel_resp.json()["status"] == "cancelled"

    # Verify listing quantity is restored to 5000.0 and active!
    restored_listing = client.get(f"/api/v1/listings/{listing_id}").json()
    assert float(restored_listing["quantity"]) == 5000.0
    assert restored_listing["status"] == "active"


def test_order_dispute_flow(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    listing_data = setup_order_prerequisites(client, db, farmer_headers)
    listing_id = listing_data["id"]

    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 500.0
    })
    order_id = order_resp.json()["id"]

    # Confirm and pay escrow
    client.post(f"/api/v1/orders/{order_id}/confirm", headers=farmer_headers)
    client.post(f"/api/v1/orders/{order_id}/pay-escrow", headers=buyer_headers)

    # Buyer raises dispute
    dispute_resp = client.post(f"/api/v1/orders/{order_id}/dispute", headers=buyer_headers, json={
        "reason": "Hosil yetkazib berilmadi yoki sifatsiz mahsulot keltirildi",
        "evidence_urls": "https://cdn.hosilbozor.uz/disputes/1.jpg"
    })
    assert dispute_resp.status_code == status.HTTP_200_OK
    assert dispute_resp.json()["status"] == "disputed"
