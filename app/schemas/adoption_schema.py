from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    pet_id: int
    adoptante_id: int
    status_id: int
    fecha_solicitud: datetime
    fecha_respuesta: Optional[datetime]
    quiere_tracker: bool

    class Config:
        from_attributes = True


