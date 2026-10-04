from datetime import date
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region


def setup_price_data(db: Session):
    region = Region(code="toshkent_sh", name_uz="Toshkent shahri", name_ru="г. Ташкент")
    db.add(region)
    db.commit()
    db.refresh(region)

    crop = Crop(slug="kartoshka", name_uz="Kartoshka", name_ru="Картофель", category="vegetables", standard_unit="kg")
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return region, crop


def test_record_market_price_admin(client: TestClient, db: Session, admin_headers: dict):
    region, crop = setup_price_data(db)

    payload = {
        "crop_id": crop.id,
        "region_id": region.id,
        "market_name": "Qo'yliq dehqon bozori",
        "min_price": 4000.0,
        "max_price": 5500.0,
        "avg_price": 4800.0,
        "recorded_date": str(date.today())
    }

    resp = client.post("/api/v1/prices", headers=admin_headers, json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert float(data["avg_price"]) == 4800.0
    assert data["market_name"] == "Qo'yliq dehqon bozori"


def test_get_daily_prices_and_history(client: TestClient, db: Session, admin_headers: dict):
    region, crop = setup_price_data(db)

    # Record price
    client.post("/api/v1/prices", headers=admin_headers, json={
        "crop_id": crop.id,
        "region_id": region.id,
        "market_name": "Parkent bozori",
        "min_price": 4200.0,
        "max_price": 5200.0,
        "avg_price": 4700.0,
        "recorded_date": str(date.today())
    })

    # Fetch daily prices
    daily_resp = client.get(f"/api/v1/prices/daily?crop_id={crop.id}")
    assert daily_resp.status_code == status.HTTP_200_OK
    daily_items = daily_resp.json()
    assert len(daily_items) >= 1
    assert float(daily_items[0]["avg_price"]) == 4700.0

    # Fetch history chart
    hist_resp = client.get(f"/api/v1/prices/history?crop_id={crop.id}&days=30")
    assert hist_resp.status_code == status.HTTP_200_OK
    hist_data = hist_resp.json()
    assert hist_data["crop_name"] == "Kartoshka"
    assert len(hist_data["history"]) >= 1


def test_csv_bulk_import(client: TestClient, db: Session, admin_headers: dict):
    region, crop = setup_price_data(db)

    csv_content = f"""crop_slug,region_code,market_name,min_price,max_price,avg_price,recorded_date
kartoshka,toshkent_sh,Chorsu bozori,4500,5500,5000,{date.today()}
kartoshka,toshkent_sh,Oloy bozori,5000,6000,5500,{date.today()}
""".encode("utf-8")

    files = {"file": ("prices.csv", csv_content, "text/csv")}
    resp = client.post("/api/v1/prices/import-csv", headers=admin_headers, files=files)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["imported"] == 2
    assert data["skipped"] == 0


def test_price_alert_subscription_flow(client: TestClient, db: Session, farmer_headers: dict):
    region, crop = setup_price_data(db)

    # 1. Subscribe to alert
    alert_resp = client.post("/api/v1/prices/alerts", headers=farmer_headers, json={
        "crop_id": crop.id,
        "region_id": region.id,
        "target_price": 6000.0,
        "condition": "above"
    })
    assert alert_resp.status_code == status.HTTP_201_CREATED
    alert_id = alert_resp.json()["id"]

    # 2. List user alerts
    list_resp = client.get("/api/v1/prices/alerts/my", headers=farmer_headers)
    assert list_resp.status_code == status.HTTP_200_OK
    assert len(list_resp.json()) >= 1

    # 3. Delete alert
    del_resp = client.delete(f"/api/v1/prices/alerts/{alert_id}", headers=farmer_headers)
    assert del_resp.status_code == status.HTTP_200_OK
    assert del_resp.json()["success"] is True
