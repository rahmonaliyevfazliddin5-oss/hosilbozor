from decimal import Decimal
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District
from app.models.order import Order


def setup_escrow_order(client: TestClient, db: Session, farmer_headers: dict, buyer_headers: dict):
    region = Region(code="andijan", name_uz="Andijon viloyati", name_ru="Андижанская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Asaka tumani", name_ru="Асакинский район")
    crop = Crop(slug="olma", name_uz="Olma", name_ru="Яблоки", category="fruits", standard_unit="kg")
    db.add_all([district, crop])
    db.commit()
    db.refresh(district)
    db.refresh(crop)

    # Farmer creates listing: 2000 kg olma @ 10,000 UZS
    listing_resp = client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": district.id,
        "quantity": 2000.0,
        "price_per_unit": 10000.0
    })
    listing_id = listing_resp.json()["id"]

    # Buyer places order for 1,000 kg
    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 1000.0,
        "delivery_amount": 200000.0
    })
    order_id = order_resp.json()["id"]

    # Farmer confirms order
    client.post(f"/api/v1/orders/{order_id}/confirm", headers=farmer_headers)

    return order_id


def test_escrow_checkout_and_mock_simulation(
    client: TestClient,
    db: Session,
    farmer_headers: dict,
    buyer_headers: dict
):
    order_id = setup_escrow_order(client, db, farmer_headers, buyer_headers)

    # 1. Create checkout invoice (mock provider)
    checkout_resp = client.post(
        f"/api/v1/payments/orders/{order_id}/checkout",
        headers=buyer_headers,
        json={"provider": "mock"}
    )
    assert checkout_resp.status_code == status.HTTP_200_OK
    invoice_data = checkout_resp.json()
    assert invoice_data["provider"] == "mock"
    assert "INV-" in invoice_data["invoice_id"]

    # 2. Simulate mock payment deposit
    sim_resp = client.post("/api/v1/payments/mock/simulate", json={
        "order_id": order_id,
        "success": True,
        "transaction_id": "MOCK-TX-12345"
    })
    assert sim_resp.status_code == status.HTTP_200_OK
    assert sim_resp.json()["success"] is True

    # 3. Check order transitioned to PAID_ESCROW
    order_detail = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    assert order_detail["status"] == "paid_escrow"

    # 4. Check escrow ledger
    ledger_resp = client.get(f"/api/v1/payments/orders/{order_id}/ledger", headers=buyer_headers)
    assert ledger_resp.status_code == status.HTTP_200_OK
    ledger_data = ledger_resp.json()
    assert float(ledger_data["held_amount"]) > 0
    assert len(ledger_data["ledger_entries"]) >= 2  # DEPOSIT and HOLD


def test_payme_and_click_webhooks(
    client: TestClient,
    db: Session,
    farmer_headers: dict,
    buyer_headers: dict
):
    order_id = setup_escrow_order(client, db, farmer_headers, buyer_headers)

    # 1. Test Payme CheckPerformTransaction
    payme_check = client.post("/api/v1/payments/webhook/payme", json={
        "method": "CheckPerformTransaction",
        "params": {"account": {"order_id": order_id}, "amount": 1020000000}
    })
    assert payme_check.status_code == status.HTTP_200_OK
    assert payme_check.json()["result"]["allow"] is True

    # 2. Test Payme PerformTransaction (Deposit funds)
    payme_perform = client.post("/api/v1/payments/webhook/payme", json={
        "method": "PerformTransaction",
        "params": {
            "id": "payme-tx-9988",
            "account": {"order_id": order_id},
            "amount": 1020000000
        }
    })
    assert payme_perform.status_code == status.HTTP_200_OK
    assert payme_perform.json()["result"]["state"] == 2

    # Check order is PAID_ESCROW
    order_detail = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    assert order_detail["status"] == "paid_escrow"


def test_escrow_release_on_order_completion(
    client: TestClient,
    db: Session,
    farmer_headers: dict,
    buyer_headers: dict
):
    order_id = setup_escrow_order(client, db, farmer_headers, buyer_headers)

    # Deposit via mock simulator
    client.post("/api/v1/payments/mock/simulate", json={"order_id": order_id, "success": True})

    order_obj = db.query(Order).filter(Order.id == order_id).first()
    pickup_code = order_obj.pickup_code
    delivery_code = order_obj.delivery_code

    # Progress: pickup -> deliver -> complete
    client.post(f"/api/v1/orders/{order_id}/verify-pickup", headers=farmer_headers, json={"pickup_code": pickup_code})
    client.post(f"/api/v1/orders/{order_id}/verify-delivery", headers=buyer_headers, json={"delivery_code": delivery_code})
    comp_resp = client.post(f"/api/v1/orders/{order_id}/complete", headers=buyer_headers)
    assert comp_resp.status_code == status.HTTP_200_OK

    # Inspect escrow ledger: should have RELEASE for seller, RELEASE for delivery, and FEE
    ledger_resp = client.get(f"/api/v1/payments/orders/{order_id}/ledger", headers=buyer_headers)
    ledger_data = ledger_resp.json()
    tx_types = [entry["transaction_type"] for entry in ledger_data["ledger_entries"]]
    assert "release" in tx_types
    assert "fee" in tx_types
    assert float(ledger_data["released_amount"]) > 0


def test_escrow_refund_on_cancellation(
    client: TestClient,
    db: Session,
    farmer_headers: dict,
    buyer_headers: dict
):
    order_id = setup_escrow_order(client, db, farmer_headers, buyer_headers)

    # Deposit via mock simulator
    client.post("/api/v1/payments/mock/simulate", json={"order_id": order_id, "success": True})

    # Cancel order
    cancel_resp = client.post(f"/api/v1/orders/{order_id}/cancel", headers=buyer_headers)
    assert cancel_resp.status_code == status.HTTP_200_OK
    assert cancel_resp.json()["status"] == "cancelled"

    # Inspect escrow ledger: should have REFUND entry
    ledger_resp = client.get(f"/api/v1/payments/orders/{order_id}/ledger", headers=buyer_headers)
    ledger_data = ledger_resp.json()
    tx_types = [entry["transaction_type"] for entry in ledger_data["ledger_entries"]]
    assert "refund" in tx_types
    assert float(ledger_data["refunded_amount"]) > 0
