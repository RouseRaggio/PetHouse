from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    nombre: str
    apellido: str
    edad: int
    usuario: str
    contrasena: str
    rol: int




