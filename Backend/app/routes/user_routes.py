from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.controllers.user_controller import (
    create_user, 
    get_users,
    get_user,
    update_user,
    delete_user,
    restore_user,
    get_user_by_email,
    login_user,

)
from app.schemas.user_schema import LoginRequest, TokenResponse

router = APIRouter(prefix="/users", tags=["Users"])


# LOGIN - Must be before {user_id} to avoid conflict
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)


# CREATE
@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# GET ALL
@router.get("/", response_model=List[UserResponse])
def read_all(db: Session = Depends(get_db)):
    return get_users(db)


# Get by email - Must be before {user_id} to avoid conflict
@router.get("/email/{email}", response_model=UserResponse)
def read_by_email(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(db, email)


# GET ONE - Must be after more specific routes
@router.get("/{user_id}", response_model=UserResponse)
def read_one(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, data)


# DELETE (Soft)
@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


# RESTORE
@router.put("/restore/{user_id}")
def restore(user_id: int, db: Session = Depends(get_db)):
    return restore_user(db, user_id)