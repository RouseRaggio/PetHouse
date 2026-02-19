from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.controllers.user_controller import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    restore_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# =========================
# CREATE
# =========================
@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# =========================
# GET ALL
# =========================
@router.get("/", response_model=list[UserResponse])
def read_all(db: Session = Depends(get_db)):
    return get_users(db)


# =========================
# GET ONE
# =========================
@router.get("/{user_id}", response_model=UserResponse)
def read_one(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


# =========================
# UPDATE
# =========================
@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


# =========================
# DELETE (soft)
# =========================
@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


# =========================
# RESTORE
# =========================
@router.put("/restore/{user_id}")
def restore(user_id: int, db: Session = Depends(get_db)):
    return restore_user(db, user_id)
