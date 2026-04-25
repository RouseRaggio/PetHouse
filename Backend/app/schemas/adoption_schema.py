from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# NESTED (para el response)
# =========================

class PetNested(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserNested(BaseModel):
    id: int
    name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class StatusNested(BaseModel):
    id: int
    name: str
    is_final: bool

    class Config:
        from_attributes = True


# =========================
# CREATE
# =========================

class AdoptionCreate(BaseModel):
    pet_id: int
    quiere_tracker: Optional[bool] = False
    cedula_url: Optional[str] = None
    recibo_url: Optional[str] = None


# =========================
# UPDATE STATUS
# =========================

class AdoptionStatusUpdate(BaseModel):
    status_id: int


# =========================
# RESPONSE
# =========================

class AdoptionResponse(BaseModel):
    id: int
    fecha_solicitud: datetime
    fecha_respuesta: Optional[datetime]
    quiere_tracker: bool
    cedula_url: Optional[str]
    recibo_url: Optional[str]

    pet: PetNested
    adoptante: UserNested
    status: StatusNested

    class Config:
        from_attributes = True