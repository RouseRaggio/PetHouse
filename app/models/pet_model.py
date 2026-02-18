from pydantic import BaseModel
from typing import Optional

class PetBase(BaseModel):
    pet_id: int
    nombre: str
    especie: str
    edad: Optional[int]
    descripcion: Optional[str]
    imagen: Optional[str]
    user_id: int