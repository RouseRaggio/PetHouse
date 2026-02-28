from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.permission_schema import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse
)
from app.controllers.permission_controller import (
    create_permission,
    get_permissions,
    get_permission,
    update_permission,
    delete_permission
)

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=PermissionResponse)
def create(data: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db, data)


@router.get("/", response_model=List[PermissionResponse])
def read_all(db: Session = Depends(get_db)):
    return get_permissions(db)


@router.get("/{permission_id}", response_model=PermissionResponse)
def read_one(permission_id: int, db: Session = Depends(get_db)):
    return get_permission(db, permission_id)


@router.put("/{permission_id}", response_model=PermissionResponse)
def update(permission_id: int, data: PermissionUpdate, db: Session = Depends(get_db)):
    return update_permission(db, permission_id, data)


@router.delete("/{permission_id}")
def delete(permission_id: int, db: Session = Depends(get_db)):
    return delete_permission(db, permission_id)