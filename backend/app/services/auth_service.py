import hashlib
import hmac
from datetime import timedelta
from typing import Tuple, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.i18n import t
from app.models.user import User, UserRole
from app.schemas.auth import Token, TelegramLoginRequest, VerifyOTPRequest
from app.schemas.user import UserCreate
from app.repositories.user_repo import user_repo
from app.services.sms_service import sms_service


class AuthService:
    def send_phone_otp(self, phone: str) -> Dict[str, Any]:
        sms_service.send_otp(phone)
        return {
            "success": True,
            "message": t("auth.otp_sent")
        }

    def verify_phone_otp(self, db: Session, payload: VerifyOTPRequest) -> Token:
        if not sms_service.verify_otp(payload.phone, payload.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=t("auth.invalid_otp")
            )

        user = user_repo.get_by_phone(db, payload.phone)
        if not user:
            user = user_repo.create(
                db,
                UserCreate(
                    phone=payload.phone,
                    full_name=payload.full_name or "Yangi Foydalanuvchi",
                    role=payload.role or UserRole.FARMER
                )
            )

        return self._generate_token_pair(user)

    def telegram_login(self, db: Session, tg_data: TelegramLoginRequest) -> Token:
        # In production, verify telegram hash with bot token sha256 HMAC
        user = user_repo.get_by_telegram_id(db, tg_data.id)
        if not user:
            full_name = f"{tg_data.first_name} {tg_data.last_name or ''}".strip()
            user = user_repo.create(
                db,
                UserCreate(
                    telegram_id=tg_data.id,
                    full_name=full_name,
                    role=tg_data.role or UserRole.FARMER
                )
            )

        return self._generate_token_pair(user)

    def refresh_access_token(self, db: Session, refresh_token_str: str) -> Token:
        try:
            payload = decode_token(refresh_token_str)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=t("auth.unauthorized")
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=t("auth.unauthorized")
                )
            user = user_repo.get_by_id(db, user_id)
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=t("auth.user_not_found")
                )
            return self._generate_token_pair(user)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=t("auth.token_expired")
            )

    def _generate_token_pair(self, user: User) -> Token:
        claims = {
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
            "phone": user.phone,
            "name": user.full_name
        }
        access_token = create_access_token(subject=user.id, extra_claims=claims)
        refresh_token = create_refresh_token(subject=user.id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )


auth_service = AuthService()
