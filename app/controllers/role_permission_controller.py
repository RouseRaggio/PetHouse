from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.role_model import Role
from app.models.permission_model import Permission


# =========================
# ASIGNAR PERMISOS A ROL
# =========================

def assign_permissions_to_role(db: Session, role_id: int, permission_ids: list):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    permissions = db.query(Permission).filter(
        Permission.id.in_(permission_ids)
    ).all()

    if not permissions:
        raise HTTPException(404, "Permisos no encontrados")

    role.permissions = permissions

    db.commit()
    db.refresh(role)

    return role


# =========================
# VER PERMISOS DE UN ROL
# =========================

def get_role_permissions(db: Session, role_id: int):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    return role.permissions