from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import (
    SendOTPRequest,
    VerifyOTPRequest,
    TelegramLoginRequest,
    RefreshTokenRequest,
    Token
)
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/send-otp", status_code=status.HTTP_200_OK)
def send_otp(payload: SendOTPRequest):
    """Initiates phone verification by generating and dispatching an SMS OTP."""
    return auth_service.send_phone_otp(payload.phone)


@router.post("/verify-otp", response_model=Token, status_code=status.HTTP_200_OK)
def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verifies OTP code and authenticates or registers user, returning JWT pair."""
    return auth_service.verify_phone_otp(db, payload)


@router.post("/telegram-login", response_model=Token, status_code=status.HTTP_200_OK)
def telegram_login(payload: TelegramLoginRequest, db: Session = Depends(get_db)):
    """Authenticates via Telegram WebApp / Bot metadata, issuing JWT pair."""
    return auth_service.telegram_login(db, payload)


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Exchanges a valid refresh token for a refreshed JWT access token."""
    return auth_service.refresh_access_token(db, payload.refresh_token)
