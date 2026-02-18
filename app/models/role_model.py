from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    role_id: int 
    nombre: str
    descripcion: Optional[str] = None