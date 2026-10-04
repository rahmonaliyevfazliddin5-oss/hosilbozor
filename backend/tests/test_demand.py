from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District


def setup_taxonomy(db: Session):
    region = Region(code="samarkand", name_uz="Samarqand viloyati", name_ru="Самаркандская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Jomboy tumani", name_ru="Джамбайский район")
    db.add(district)

    crop = Crop(slug="piyoz", name_uz="Piyoz", name_ru="Лук", category="vegetables", standard_unit="kg")
    db.add(crop)
    db.commit()
    db.refresh(district)
    db.refresh(crop)
    return district, crop


def test_reverse_auction_flow(client: TestClient, db: Session, buyer_headers: dict, farmer_headers: dict):
    district, crop = setup_taxonomy(db)

    # 1. Buyer posts demand: 50,000 kg piyoz needed
    demand_payload = {
        "crop_id": crop.id,
        "destination_district_id": district.id,
        "target_quantity": 50000.0,
        "max_price_per_unit": 2500.0,
        "description": "Eksport uchun sifatli piyoz kerak"
    }
    demand_resp = client.post("/api/v1/demand", headers=buyer_headers, json=demand_payload)
    assert demand_resp.status_code == status.HTTP_201_CREATED
    demand_data = demand_resp.json()
    demand_id = demand_data["id"]
    assert demand_data["status"] == "active"
    assert demand_data["buyer"]["full_name"] == "Bobur Savdogar"

    # 2. Farmer submits an offer
    offer_payload = {
        "offered_price_per_unit": 2300.0,
        "offered_quantity": 50000.0,
        "notes": "Birinchi navli sariq piyoz, yetkazib berishga tayyor"
    }
    offer_resp = client.post(f"/api/v1/demand/{demand_id}/offers", headers=farmer_headers, json=offer_payload)
    assert offer_resp.status_code == status.HTTP_201_CREATED
    offer_data = offer_resp.json()
    offer_id = offer_data["id"]
    assert float(offer_data["offered_price_per_unit"]) == 2300.0
    assert offer_data["status"] == "pending"

    # 3. Check demand shows the offer
    get_demand = client.get(f"/api/v1/demand/{demand_id}")
    assert get_demand.status_code == status.HTTP_200_OK
    assert get_demand.json()["offers_count"] == 1

    # 4. Buyer accepts the farmer's offer -> Creates Order!
    accept_resp = client.post(f"/api/v1/demand/offers/{offer_id}/accept", headers=buyer_headers)
    assert accept_resp.status_code == status.HTTP_201_CREATED
    order_data = accept_resp.json()
    assert order_data["status"] == "created"
    assert float(order_data["quantity"]) == 50000.0
    assert float(order_data["price_per_unit"]) == 2300.0
    assert "HB-" in order_data["order_number"]

    # 5. Verify demand is fulfilled
    updated_demand = client.get(f"/api/v1/demand/{demand_id}").json()
    assert updated_demand["status"] == "fulfilled"
