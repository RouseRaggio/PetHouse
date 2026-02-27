from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# CREATE
# =========================

class RoleCreate(BaseModel):
    name: str


# =========================
# UPDATE
# =========================

class RoleUpdate(BaseModel):
    name: Optional[str]


# =========================
# RESPONSE
# =========================

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True