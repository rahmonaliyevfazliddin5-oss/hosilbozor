from typing import List
from pydantic import BaseModel


class DistrictRead(BaseModel):
    id: str
    region_id: str
    name_uz: str
    name_ru: str

    class Config:
        from_attributes = True


class RegionRead(BaseModel):
    id: str
    code: str
    name_uz: str
    name_ru: str
    districts: List[DistrictRead] = []

    class Config:
        from_attributes = True


class CropRead(BaseModel):
    id: str
    slug: str
    name_uz: str
    name_ru: str
    category: str
    standard_unit: str

    class Config:
        from_attributes = True
