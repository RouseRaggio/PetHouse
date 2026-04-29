from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# CREATE
# =========================

class UserCreate(BaseModel):
    role_id: int
    name: str
    last_name: str
    email: EmailStr
    password: str


# =========================
# UPDATE
# =========================

class UserUpdate(BaseModel):
    role_id: Optional[int]
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]


# =========================
# RESPONSE
# =========================

class UserResponse(BaseModel):
    id: int
    role_id: int
    name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse