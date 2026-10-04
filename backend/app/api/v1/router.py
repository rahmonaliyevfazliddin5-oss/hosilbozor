from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, meta, listings, prices, demand, orders, logistics, payments

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(listings.router, prefix="/listings", tags=["listings"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
api_router.include_router(demand.router, prefix="/demand", tags=["demand"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["logistics"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
