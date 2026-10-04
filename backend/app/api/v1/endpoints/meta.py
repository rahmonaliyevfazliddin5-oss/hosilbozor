from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.region import Region, District
from app.models.crop import Crop
from app.schemas.meta import RegionRead, CropRead

router = APIRouter()


@router.get("/regions", response_model=List[RegionRead])
def list_regions(db: Session = Depends(get_db)):
    """Returns list of all Uzbekistan regions with nested districts."""
    return db.query(Region).all()


@router.get("/crops", response_model=List[CropRead])
def list_crops(db: Session = Depends(get_db)):
    """Returns available agricultural crop categories and units."""
    return db.query(Crop).all()
