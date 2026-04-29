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
    name: Optional[str]
    species: Optional[str]
    race: Optional[str]
    birth_date: Optional[datetime]
    gender: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    status: Optional[str]


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
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True