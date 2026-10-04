from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District


def setup_logistics_scenario(client: TestClient, db: Session, farmer_headers: dict, driver_headers: dict, buyer_headers: dict):
    # 1. Setup regions & crop
    region = Region(code="tashkent_reg", name_uz="Toshkent viloyati", name_ru="Ташкентская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    dist_origin = District(region_id=region.id, name_uz="Bekobod tumani", name_ru="Бекабадский район")
    dist_dest = District(region_id=region.id, name_uz="Chinoz tumani", name_ru="Чиназский район")
    crop = Crop(slug="tarvuz", name_uz="Tarvuz", name_ru="Арбуз", category="fruits", standard_unit="kg")
    db.add_all([dist_origin, dist_dest, crop])
    db.commit()
    db.refresh(dist_origin)
    db.refresh(dist_dest)
    db.refresh(crop)

    # 2. Driver registers vehicle
    veh_resp = client.post("/api/v1/users/profile/driver/vehicles", headers=driver_headers, json={
        "vehicle_type": "Gazel Next",
        "plate_number": "10 B 777 BB",
        "capacity_tons": 3.5,
        "is_refrigerated": False
    })
    vehicle_id = veh_resp.json()["id"]

    # 3. Farmer lists harvest
    listing_resp = client.post("/api/v1/listings", headers=farmer_headers, json={
        "crop_id": crop.id,
        "district_id": dist_origin.id,
        "quantity": 10000.0,
        "price_per_unit": 2000.0
    })
    listing_id = listing_resp.json()["id"]

    # 4. Buyer creates order for 3,000 kg
    order_resp = client.post("/api/v1/orders/from-listing", headers=buyer_headers, json={
        "listing_id": listing_id,
        "quantity": 3000.0
    })
    order_id = order_resp.json()["id"]

    return order_id, vehicle_id, dist_origin.id, dist_dest.id


def test_logistics_end_to_end_workflow(
    client: TestClient,
    db: Session,
    farmer_headers: dict,
    driver_headers: dict,
    buyer_headers: dict
):
    order_id, vehicle_id, origin_id, dest_id = setup_logistics_scenario(
        client, db, farmer_headers, driver_headers, buyer_headers
    )

    # 1. Create delivery job for order
    job_resp = client.post("/api/v1/logistics/jobs", headers=buyer_headers, json={
        "order_id": order_id,
        "proposed_price": 800000.0,
        "pickup_district_id": origin_id,
        "delivery_district_id": dest_id
    })
    assert job_resp.status_code == status.HTTP_201_CREATED
    job_data = job_resp.json()
    job_id = job_data["id"]
    assert job_data["status"] == "open"

    # 2. Driver lists available open delivery jobs
    open_jobs = client.get("/api/v1/logistics/jobs?status=open")
    assert open_jobs.status_code == status.HTTP_200_OK
    assert open_jobs.json()["total"] >= 1

    # 3. Driver submits a bid
    bid_resp = client.post(f"/api/v1/logistics/jobs/{job_id}/bids", headers=driver_headers, json={
        "vehicle_id": vehicle_id,
        "bid_amount": 750000.0,
        "estimated_hours": 4
    })
    assert bid_resp.status_code == status.HTTP_201_CREATED
    bid_data = bid_resp.json()
    bid_id = bid_data["id"]
    assert float(bid_data["bid_amount"]) == 750000.0
    assert bid_data["status"] == "pending"

    # 4. Buyer accepts driver's bid
    accept_resp = client.post(f"/api/v1/logistics/bids/{bid_id}/accept", headers=buyer_headers)
    assert accept_resp.status_code == status.HTTP_200_OK
    assigned_job = accept_resp.json()
    assert assigned_job["status"] == "assigned"
    assert float(assigned_job["agreed_price"]) == 750000.0

    # 5. Order delivery fee updated
    order_check = client.get(f"/api/v1/orders/{order_id}", headers=buyer_headers).json()
    assert float(order_check["delivery_amount"]) == 750000.0

    # 6. Driver starts trip
    start_resp = client.post(
        f"/api/v1/logistics/jobs/{job_id}/start?proof_url=https://cdn.hosilbozor.uz/pickup.jpg",
        headers=driver_headers
    )
    assert start_resp.status_code == status.HTTP_200_OK
    assert start_resp.json()["status"] == "in_transit"
    assert start_resp.json()["pickup_proof_url"] == "https://cdn.hosilbozor.uz/pickup.jpg"

    # 7. Driver completes delivery
    deliver_resp = client.post(
        f"/api/v1/logistics/jobs/{job_id}/deliver?proof_url=https://cdn.hosilbozor.uz/delivered.jpg",
        headers=driver_headers
    )
    assert deliver_resp.status_code == status.HTTP_200_OK
    assert deliver_resp.json()["status"] == "delivered"
    assert deliver_resp.json()["delivery_proof_url"] == "https://cdn.hosilbozor.uz/delivered.jpg"

    # 8. Check driver trips list
    my_trips = client.get("/api/v1/logistics/my-trips", headers=driver_headers)
    assert my_trips.status_code == status.HTTP_200_OK
    assert my_trips.json()["total"] >= 1
