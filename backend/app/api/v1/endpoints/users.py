from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.profile import FarmerProfile, BuyerProfile, DriverProfile, Vehicle
from app.schemas.user import UserRead, UserUpdate, RoleChangeRequest
from app.schemas.profile import (
    FarmerProfileRead,
    FarmerProfileUpdate,
    BuyerProfileRead,
    BuyerProfileUpdate,
    DriverProfileRead,
    DriverProfileUpdate,
    VehicleCreate,
    VehicleRead
)
from app.repositories.user_repo import user_repo

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Returns the authenticated user profile."""
    return current_user


@router.patch("/me", response_model=UserRead)
def update_current_user_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates language preference, full name, or active role."""
    return user_repo.update(db, current_user, payload)


@router.post("/switch-role", response_model=UserRead)
def switch_active_role(
    payload: RoleChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dynamically activates or switches persona role (farmer, buyer, driver)."""
    current_user.role = payload.role
    db.commit()
    db.refresh(current_user)
    user_repo.ensure_role_profile(db, current_user)
    return current_user


# Farmer Profile Endpoints
@router.get("/profile/farmer", response_model=FarmerProfileRead)
def get_farmer_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    if not profile:
        profile = FarmerProfile(user_id=current_user.id, farm_name=f"{current_user.full_name} xo'jaligi")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/profile/farmer", response_model=FarmerProfileRead)
def update_farmer_profile(
    payload: FarmerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    if not profile:
        profile = FarmerProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


# Buyer Profile Endpoints
@router.get("/profile/buyer", response_model=BuyerProfileRead)
def get_buyer_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(BuyerProfile).filter(BuyerProfile.user_id == current_user.id).first()
    if not profile:
        profile = BuyerProfile(user_id=current_user.id, company_name=current_user.full_name)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/profile/buyer", response_model=BuyerProfileRead)
def update_buyer_profile(
    payload: BuyerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(BuyerProfile).filter(BuyerProfile.user_id == current_user.id).first()
    if not profile:
        profile = BuyerProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


# Driver Profile Endpoints
@router.get("/profile/driver", response_model=DriverProfileRead)
def get_driver_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
    if not profile:
        profile = DriverProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/profile/driver", response_model=DriverProfileRead)
def update_driver_profile(
    payload: DriverProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
    if not profile:
        profile = DriverProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/profile/driver/vehicles", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def add_driver_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
    if not profile:
        profile = DriverProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    vehicle = Vehicle(
        driver_id=profile.id,
        vehicle_type=payload.vehicle_type,
        plate_number=payload.plate_number,
        capacity_tons=payload.capacity_tons,
        volume_m3=payload.volume_m3,
        is_refrigerated=payload.is_refrigerated
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
