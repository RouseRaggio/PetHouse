from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.role_permission_schema import AssignPermissions
from app.schemas.permission_schema import PermissionResponse
from app.controllers.role_permission_controller import (
    assign_permissions_to_role,
    get_role_permissions
)

router = APIRouter(prefix="/roles", tags=["Role Permissions"])


@router.post("/{role_id}/permissions")
def assign_permissions(
    role_id: int,
    data: AssignPermissions,
    db: Session = Depends(get_db)
):
    return assign_permissions_to_role(db, role_id, data.permission_ids)


@router.get("/{role_id}/permissions", response_model=List[PermissionResponse])
def read_role_permissions(
    role_id: int,
    db: Session = Depends(get_db)
):
    return get_role_permissions(db, role_id) 