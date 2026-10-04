from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import decode_token


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "HosilBozor"


def test_send_otp_success(client: TestClient):
    response = client.post("/api/v1/auth/send-otp", json={"phone": "+998901234567"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True


def test_send_otp_invalid_phone(client: TestClient):
    response = client.post("/api/v1/auth/send-otp", json={"phone": "12345"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_verify_otp_valid(client: TestClient):
    # Request OTP
    client.post("/api/v1/auth/send-otp", json={"phone": "+998909876543"})
    
    # Verify with mock code '1234'
    verify_resp = client.post("/api/v1/auth/verify-otp", json={
        "phone": "+998909876543",
        "code": "1234",
        "role": "farmer",
        "full_name": "Rustam Dehqon"
    })
    assert verify_resp.status_code == status.HTTP_200_OK
    data = verify_resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify token payload
    payload = decode_token(data["access_token"])
    assert payload["role"] == "farmer"


def test_verify_otp_invalid_code(client: TestClient):
    verify_resp = client.post("/api/v1/auth/verify-otp", json={
        "phone": "+998909876543",
        "code": "0000"  # Invalid code
    })
    assert verify_resp.status_code == status.HTTP_400_BAD_REQUEST


def test_telegram_login_new_user(client: TestClient):
    tg_payload = {
        "id": 123456789,
        "first_name": "Sherzod",
        "last_name": "Qodirov",
        "username": "sherzod_fermer",
        "auth_date": 1700000000,
        "hash": "mock_hash_for_testing",
        "role": "farmer"
    }
    response = client.post("/api/v1/auth/telegram-login", json=tg_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_rotation(client: TestClient):
    # Login first
    verify_resp = client.post("/api/v1/auth/verify-otp", json={
        "phone": "+998905556677",
        "code": "1234",
        "role": "buyer",
        "full_name": "Akbar Savdo"
    })
    refresh_token = verify_resp.json()["refresh_token"]

    # Exchange for new token
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == status.HTTP_200_OK
    new_data = refresh_resp.json()
    assert "access_token" in new_data
    assert "refresh_token" in new_data
