from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import hash_password, verify_password


def test_get_me_unauthorized(client: TestClient):
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_me_authorized(client: TestClient, farmer_headers: dict, farmer_user):
    response = client.get("/api/v1/users/me", headers=farmer_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == farmer_user.id
    assert data["phone"] == farmer_user.phone
    assert data["full_name"] == farmer_user.full_name
    assert data["role"] == "farmer"


def test_patch_me(client: TestClient, farmer_headers: dict):
    response = client.patch(
        "/api/v1/users/me",
        headers=farmer_headers,
        json={"full_name": "Alisher Yangilangan", "language": "ru"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Alisher Yangilangan"
    assert data["language"] == "ru"


def test_switch_role(client: TestClient, farmer_headers: dict):
    response = client.post(
        "/api/v1/users/switch-role",
        headers=farmer_headers,
        json={"role": "driver"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["role"] == "driver"


def test_farmer_profile_crud(client: TestClient, farmer_headers: dict):
    get_resp = client.get("/api/v1/users/profile/farmer", headers=farmer_headers)
    assert get_resp.status_code == status.HTTP_200_OK
    
    put_resp = client.put(
        "/api/v1/users/profile/farmer",
        headers=farmer_headers,
        json={"farm_name": "Agro Baraka MCHJ"}
    )
    assert put_resp.status_code == status.HTTP_200_OK
    assert put_resp.json()["farm_name"] == "Agro Baraka MCHJ"


def test_buyer_profile_crud(client: TestClient, buyer_headers: dict):
    get_resp = client.get("/api/v1/users/profile/buyer", headers=buyer_headers)
    assert get_resp.status_code == status.HTTP_200_OK

    put_resp = client.put(
        "/api/v1/users/profile/buyer",
        headers=buyer_headers,
        json={"company_name": "Toshkent Mega Agro MCHJ", "buyer_type": "wholesale"}
    )
    assert put_resp.status_code == status.HTTP_200_OK
    assert put_resp.json()["company_name"] == "Toshkent Mega Agro MCHJ"


def test_driver_profile_crud(client: TestClient, driver_user):
    from app.core.security import create_access_token
    token = create_access_token(subject=driver_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    get_resp = client.get("/api/v1/users/profile/driver", headers=headers)
    assert get_resp.status_code == status.HTTP_200_OK

    put_resp = client.put(
        "/api/v1/users/profile/driver",
        headers=headers,
        json={"license_number": "AA1234567", "is_available": True}
    )
    assert put_resp.status_code == status.HTTP_200_OK
    assert put_resp.json()["license_number"] == "AA1234567"


def test_driver_vehicle_registration(client: TestClient, driver_user, db):
    from app.core.security import create_access_token
    token = create_access_token(subject=driver_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    veh_resp = client.post(
        "/api/v1/users/profile/driver/vehicles",
        headers=headers,
        json={
            "vehicle_type": "Isuzu NPR",
            "plate_number": "01 A 777 AA",
            "capacity_tons": 5.0,
            "volume_m3": 18.5,
            "is_refrigerated": True
        }
    )
    assert veh_resp.status_code == status.HTTP_201_CREATED
    data = veh_resp.json()
    assert data["vehicle_type"] == "Isuzu NPR"
    assert data["capacity_tons"] == 5.0
    assert data["is_refrigerated"] is True


def test_password_hashing():
    pw = "SecretPass123!"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPass", hashed) is False
