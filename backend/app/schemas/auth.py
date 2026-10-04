from typing import Optional
from pydantic import BaseModel, Field
from app.models.user import UserRole


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class SendOTPRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+998[0-9]{9}$", examples=["+998901234567"])


class VerifyOTPRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+998[0-9]{9}$", examples=["+998901234567"])
    code: str = Field(..., min_length=4, max_length=6, examples=["1234"])
    role: Optional[UserRole] = UserRole.FARMER
    full_name: Optional[str] = "Yangi Foydalanuvchi"


class TelegramLoginRequest(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str
    role: Optional[UserRole] = UserRole.FARMER


class RefreshTokenRequest(BaseModel):
    refresh_token: str
