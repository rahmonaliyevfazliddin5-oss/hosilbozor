from fastapi import status, Depends, APIRouter
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.api.deps import require_role
from app.models.user import UserRole
from app.models.region import Region, District
from app.models.crop import Crop

# Ephemeral test router to strictly test require_role guards
test_rbac_router = APIRouter()


@test_rbac_router.get("/test/farmer-only", dependencies=[Depends(require_role([UserRole.FARMER]))])
def farmer_only():
    return {"message": "farmer access granted"}


@test_rbac_router.get("/test/driver-only", dependencies=[Depends(require_role([UserRole.DRIVER]))])
def driver_only():
    return {"message": "driver access granted"}


app.include_router(test_rbac_router)


def test_rbac_guard_enforcement(client: TestClient, farmer_headers: dict, buyer_headers: dict):
    # Farmer accessing farmer endpoint -> 200 OK
    resp_farmer = client.get("/test/farmer-only", headers=farmer_headers)
    assert resp_farmer.status_code == status.HTTP_200_OK

    # Buyer attempting to access farmer endpoint -> 403 Forbidden
    resp_buyer = client.get("/test/farmer-only", headers=buyer_headers)
    assert resp_buyer.status_code == status.HTTP_403_FORBIDDEN


def test_meta_regions_and_crops(client: TestClient, db: Session):
    # Seed a sample region & district
    region = Region(code="tashkent", name_uz="Toshkent viloyati", name_ru="Ташкентская область")
    db.add(region)
    db.commit()
    db.refresh(region)

    district = District(region_id=region.id, name_uz="Parkent tumani", name_ru="Паркентский район")
    db.add(district)

    # Seed a sample crop
    crop = Crop(slug="pomidor", name_uz="Pomidor", name_ru="Помидоры", category="vegetables", standard_unit="kg")
    db.add(crop)
    db.commit()

    # Query meta endpoints
    regions_resp = client.get("/api/v1/meta/regions")
    assert regions_resp.status_code == status.HTTP_200_OK
    regions_data = regions_resp.json()
    assert len(regions_data) >= 1
    assert regions_data[0]["name_uz"] == "Toshkent viloyati"
    assert len(regions_data[0]["districts"]) >= 1
    assert regions_data[0]["districts"][0]["name_uz"] == "Parkent tumani"

    crops_resp = client.get("/api/v1/meta/crops")
    assert crops_resp.status_code == status.HTTP_200_OK
    crops_data = crops_resp.json()
    assert len(crops_data) >= 1
    assert crops_data[0]["slug"] == "pomidor"
