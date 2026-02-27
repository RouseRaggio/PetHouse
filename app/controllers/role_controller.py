from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.role_model import Role
from app.schemas.role_schema import RoleCreate, RoleUpdate


# =========================
# CREATE
# =========================

def create_role(db: Session, data: RoleCreate):

    existing = db.query(Role).filter(
        Role.name == data.name,
        Role.deleted_at == None
    ).first()

    if existing:
        raise HTTPException(400, "Rol ya existe")

    role = Role(name=data.name)

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


# =========================
# GET ALL
# =========================

def get_roles(db: Session):

    return db.query(Role).filter(
        Role.deleted_at == None
    ).all()


# =========================
# GET ONE
# =========================

def get_role(db: Session, role_id: int):

    role = db.query(Role).filter(
        Role.id == role_id,
        Role.deleted_at == None
    ).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    return role


# =========================
# UPDATE
# =========================

def update_role(db: Session, role_id: int, data: RoleUpdate):

    role = db.query(Role).filter(
        Role.id == role_id,
        Role.deleted_at == None
    ).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    if data.name:
        role.name = data.name

    db.commit()
    db.refresh(role)

    return role


# =========================
# SOFT DELETE
# =========================

def delete_role(db: Session, role_id: int):

    role = db.query(Role).filter(
        Role.id == role_id,
        Role.deleted_at == None
    ).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    role.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Rol eliminado lógicamente"}