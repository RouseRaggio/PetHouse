from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# CREATE
# =========================

class PetCreate(BaseModel):
    name: str
    species: str
    race: Optional[str]
    birth_date: Optional[datetime]
    gender: Optional[str]
    description: Optional[str]
    image_url: Optional[str]


# =========================
# UPDATE
# =========================

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    race: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    gps_status: Optional[str] = None
    gps_imei: Optional[str] = None


# =========================
# RESPONSE
# =========================

class PetResponse(BaseModel):
    id: int
    publisher_id: int
    name: str
    species: str
    race: Optional[str]
    birth_date: Optional[datetime]
    gender: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    status: Optional[str]
    gps_status: Optional[str] = "none"
    gps_imei: Optional[str] = None
    adopter_name: Optional[str] = None
    adopter_id: Optional[int] = None
    publisher_name: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True