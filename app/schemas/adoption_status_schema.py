from pydantic import BaseModel
from typing import Optional


# =========================
# CREATE
# =========================

class AdoptionStatusCreate(BaseModel):
    name: str
    is_final: bool = False
    order: int


# =========================
# UPDATE
# =========================

class AdoptionStatusUpdate(BaseModel):
    name: Optional[str] = None
    is_final: Optional[bool] = None
    order: Optional[int] = None


# =========================
# RESPONSE
# =========================

class AdoptionStatusResponse(BaseModel):
    id: int
    name: str
    is_final: bool
    order: int

    class Config:
        from_attributes = True