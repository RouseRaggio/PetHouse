from pydantic import BaseModel
from typing import Optional, List

class PermissionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None