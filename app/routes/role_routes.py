from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.role_schema import RoleCreate, RoleUpdate, RoleResponse
from app.controllers.role_controller import (
    create_role,
    get_roles,
    get_role,
    update_role,
    delete_role
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleResponse)
def create(data: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, data)


@router.get("/", response_model=List[RoleResponse])
def read_all(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get("/{role_id}", response_model=RoleResponse)
def read_one(role_id: int, db: Session = Depends(get_db)):
    return get_role(db, role_id)


@router.put("/{role_id}", response_model=RoleResponse)
def update(role_id: int, data: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(db, role_id, data)


@router.delete("/{role_id}")
def delete(role_id: int, db: Session = Depends(get_db)):
    return delete_role(db, role_id)