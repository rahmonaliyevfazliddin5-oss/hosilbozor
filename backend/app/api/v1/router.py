from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, meta, listings, prices

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(listings.router, prefix="/listings", tags=["listings"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
