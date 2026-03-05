from pydantic import BaseModel
from typing import Optional


# =========================
# CREATE
# =========================

class PermissionCreate(BaseModel):
    name: str


# =========================
# UPDATE
# =========================

class PermissionUpdate(BaseModel):
    name: Optional[str] = None


# =========================
# RESPONSE
# =========================

class PermissionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True