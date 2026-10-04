from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.profile import FarmerProfile, BuyerProfile, DriverProfile
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def get_by_id(self, db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        return db.query(User).filter(User.phone == phone).first()

    def get_by_telegram_id(self, db: Session, telegram_id: int) -> Optional[User]:
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def create(self, db: Session, user_in: UserCreate) -> User:
        user = User(
            phone=user_in.phone,
            telegram_id=user_in.telegram_id,
            full_name=user_in.full_name,
            language=user_in.language,
            role=user_in.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        self.ensure_role_profile(db, user)
        return user

    def update(self, db: Session, user: User, update_data: UserUpdate) -> User:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        if "role" in update_dict:
            self.ensure_role_profile(db, user)
        return user

    def ensure_role_profile(self, db: Session, user: User) -> None:
        if user.role == UserRole.FARMER and not user.farmer_profile:
            profile = FarmerProfile(user_id=user.id, farm_name=f"{user.full_name} xo'jaligi")
            db.add(profile)
            db.commit()
        elif user.role == UserRole.BUYER and not user.buyer_profile:
            profile = BuyerProfile(user_id=user.id, company_name=user.full_name)
            db.add(profile)
            db.commit()
        elif user.role == UserRole.DRIVER and not user.driver_profile:
            profile = DriverProfile(user_id=user.id)
            db.add(profile)
            db.commit()

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()


user_repo = UserRepository()
