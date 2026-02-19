# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    role_id: int



class UserCreate(UserBase):
    password: str



class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    activo: Optional[bool] = None




class UserResponse(UserBase):
    id: int
    activo: bool
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  
 