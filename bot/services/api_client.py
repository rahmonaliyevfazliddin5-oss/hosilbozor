import httpx
from typing import Optional, Dict, Any, List


class BackendAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url

    async def telegram_login(self, telegram_id: int, first_name: str, username: Optional[str] = None, role: str = "farmer") -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/auth/telegram-login",
                json={
                    "id": telegram_id,
                    "first_name": first_name,
                    "username": username,
                    "auth_date": 1700000000,
                    "hash": "tg_verified",
                    "role": role
                }
            )
            resp.raise_for_status()
            return resp.json()

    async def get_crops(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/meta/crops")
            if resp.status_code == 200:
                return resp.json()
            return []

    async def get_daily_prices(self, crop_id: Optional[str] = None) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/prices/daily"
            if crop_id:
                url += f"?crop_id={crop_id}"
            resp = await client.get(url)
            if resp.status_code == 200:
                return resp.json()
            return []

    async def create_listing(self, access_token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/listings", headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def get_open_delivery_jobs(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/logistics/jobs?status=open")
            if resp.status_code == 200:
                return resp.json().get("items", [])
            return []

    async def submit_bid(self, access_token: str, job_id: str, vehicle_id: str, bid_amount: float) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/logistics/jobs/{job_id}/bids",
                headers=headers,
                json={"vehicle_id": vehicle_id, "bid_amount": bid_amount}
            )
            resp.raise_for_status()
            return resp.json()

    async def verify_pickup_code(self, access_token: str, order_id: str, code: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/orders/{order_id}/verify-pickup",
                headers=headers,
                json={"pickup_code": code}
            )
            resp.raise_for_status()
            return resp.json()

    async def verify_delivery_code(self, access_token: str, order_id: str, code: str, photo_url: Optional[str] = None) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/orders/{order_id}/verify-delivery",
                headers=headers,
                json={"delivery_code": code, "proof_photo_url": photo_url}
            )
            resp.raise_for_status()
            return resp.json()


api_client = BackendAPIClient()
