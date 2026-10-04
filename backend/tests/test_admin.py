from decimal import Decimal
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District
from app.models.order import OrderStatus


def setup_order_for_dispute(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    # Setup region, district and crop
    region = Region(code="toshkent_sh", name_uz="Toshkent shahri", name_ru="г. Ташкент")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Chilonzor tumani", name_ru="Чиланзарский район")
    db.add(district)

    crop = Crop(slug="pomidor", name_uz="Pomidor", name_ru="Томаты", category="vegetables", standard_unit="kg")
    db.add(crop)
    db.commit()
    db.refresh(district)
    db.refresh(crop)

    # Create listing
    listing_resp = client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 1000.0,
        "min_order_quantity": 100.0,
        "price_per_unit": 8000.0,
        "quality_grade": "premium",
        "description": "Issiqxona pomidori"
    })
    listing_id = listing_resp.json()["id"]

    # Buyer creates order
    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 200.0
    })
    order_id = order_resp.json()["id"]

    # Confirm and pay escrow
    client.post(f"/api/v1/orders/{order_id}/confirm", headers=farmer_headers)
    client.post(f"/api/v1/orders/{order_id}/pay-escrow", headers=buyer_headers)

    # Raise dispute
    client.post(f"/api/v1/orders/{order_id}/dispute", headers=buyer_headers, json={
        "reason": "Yetkazilgan hosil talabga javob bermaydi",
        "evidence_urls": "https://img.uz/dispute1.jpg"
    })

    return order_id


def test_admin_metrics_rbac(client: TestClient, farmer_headers: dict, admin_headers: dict):
    # Farmer forbidden
    resp_farmer = client.get("/api/v1/admin/metrics", headers=farmer_headers)
    assert resp_farmer.status_code == status.HTTP_403_FORBIDDEN

    # Admin allowed
    resp_admin = client.get("/api/v1/admin/metrics", headers=admin_headers)
    assert resp_admin.status_code == status.HTTP_200_OK
    data = resp_admin.json()
    assert "total_gmv_uzs" in data
    assert "total_orders" in data
    assert "fill_rate_percent" in data
    assert "total_users" in data
    assert "active_farmers" in data
    assert "avg_price_spread_percent" in data


def test_admin_verification_queue_and_verify(client: TestClient, buyer_user, admin_headers: dict, buyer_headers: dict):
    # Buyer forbidden to access queue
    forbidden = client.get("/api/v1/admin/users/verification-queue", headers=buyer_headers)
    assert forbidden.status_code == status.HTTP_403_FORBIDDEN

    # Admin gets verification queue
    queue_resp = client.get("/api/v1/admin/users/verification-queue", headers=admin_headers)
    assert queue_resp.status_code == status.HTTP_200_OK
    queue = queue_resp.json()
    queue_ids = [u["id"] for u in queue]
    assert buyer_user.id in queue_ids

    # Admin verifies buyer
    verify_resp = client.post(f"/api/v1/admin/users/{buyer_user.id}/verify", headers=admin_headers)
    assert verify_resp.status_code == status.HTTP_200_OK
    assert verify_resp.json()["is_verified"] is True

    # Check buyer is no longer in unverified queue
    queue_resp2 = client.get("/api/v1/admin/users/verification-queue", headers=admin_headers)
    queue2 = queue_resp2.json()
    queue2_ids = [u["id"] for u in queue2]
    assert buyer_user.id not in queue2_ids


def test_admin_dispute_resolution_release_to_seller(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict, admin_headers: dict):
    order_id = setup_order_for_dispute(client, db, farmer_headers, buyer_headers)

    # Admin lists disputes
    disputes_resp = client.get("/api/v1/admin/disputes", headers=admin_headers)
    assert disputes_resp.status_code == status.HTTP_200_OK
    disputes = disputes_resp.json()
    assert len(disputes) >= 1
    target_dispute = next(d for d in disputes if d["order_id"] == order_id)
    assert target_dispute["status"] == "opened"

    # Admin resolves dispute in favor of seller (release funds)
    resolve_resp = client.post(
        f"/api/v1/admin/disputes/{target_dispute['id']}/resolve",
        headers=admin_headers,
        json={
            "action": "release_to_seller",
            "resolution_notes": "Ekspertiza natijasida hosil sifati standartga mos deb topildi."
        }
    )
    assert resolve_resp.status_code == status.HTTP_200_OK
    resolved_data = resolve_resp.json()
    assert resolved_data["status"] == "resolved_release"

    # Check order is marked COMPLETED
    order_check = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    assert order_check["status"] == OrderStatus.COMPLETED.value

    # Check escrow ledger: released amount > 0
    escrow_check = client.get(f"/api/v1/payments/orders/{order_id}/ledger", headers=buyer_headers).json()
    assert float(escrow_check["released_amount"]) > 0


def test_admin_dispute_resolution_refund_to_buyer(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict, admin_headers: dict):
    order_id = setup_order_for_dispute(client, db, farmer_headers, buyer_headers)

    disputes_resp = client.get("/api/v1/admin/disputes", headers=admin_headers)
    target_dispute = next(d for d in disputes_resp.json() if d["order_id"] == order_id)

    # Admin resolves dispute in favor of buyer (refund)
    resolve_resp = client.post(
        f"/api/v1/admin/disputes/{target_dispute['id']}/resolve",
        headers=admin_headers,
        json={
            "action": "refund_to_buyer",
            "resolution_notes": "Yuk yetkazib berilmaganligi tasdiqlandi. Mablag' xaridorga qaytarildi."
        }
    )
    assert resolve_resp.status_code == status.HTTP_200_OK
    assert resolve_resp.json()["status"] == "resolved_refund"

    # Check order is CANCELLED
    order_check = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    assert order_check["status"] == OrderStatus.CANCELLED.value

    # Check escrow ledger: refunded amount > 0
    escrow_check = client.get(f"/api/v1/payments/orders/{order_id}/ledger", headers=buyer_headers).json()
    assert float(escrow_check["refunded_amount"]) > 0
