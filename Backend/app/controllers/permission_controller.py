from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.permission_model import Permission


# =========================
# CREATE
# =========================

def create_permission(db: Session, data):

    existing = db.query(Permission).filter(
        Permission.name == data.name.upper()
    ).first()

    if existing:
        raise HTTPException(400, "Este permiso ya existe")

    permission = Permission(
        name=data.name.upper()
    )

    db.add(permission)
    db.commit()
    db.refresh(permission)

    return permission


# =========================
# GET ALL
# =========================

def get_permissions(db: Session):
    return db.query(Permission).all()


# =========================
# GET ONE
# =========================

def get_permission(db: Session, permission_id: int):

    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()

    if not permission:
        raise HTTPException(404, "Permiso no encontrado")

    return permission


# =========================
# UPDATE
# =========================

def update_permission(db: Session, permission_id: int, data):

    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()

    if not permission:
        raise HTTPException(404, "Permiso no encontrado")

    if data.name:
        permission.name = data.name.upper()

    db.commit()
    db.refresh(permission)

    return permission


# =========================
# DELETE
# =========================

def delete_permission(db: Session, permission_id: int):

    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()

    if not permission:
        raise HTTPException(404, "Permiso no encontrado")

    db.delete(permission)
    db.commit()

    return {"message": "Permiso eliminado correctamente"}