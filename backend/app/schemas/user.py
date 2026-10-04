from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.user import UserRole


class UserBase(BaseModel):
    phone: Optional[str] = None
    telegram_id: Optional[int] = None
    full_name: str
    language: str = "uz_latn"
    role: UserRole = UserRole.FARMER


class UserCreate(UserBase):
    password: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    language: Optional[str] = None
    role: Optional[UserRole] = None


class RoleChangeRequest(BaseModel):
    role: UserRole


class UserRead(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
