from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password
from app.core.security import verify_password
from app.auth.jwt_handler import create_access_token


# =========================
# CREATE
# =========================

def create_user(db: Session, user: UserCreate):

    existing = db.query(User).filter(
        User.email == user.email,
        User.deleted_at == None
    ).first()

    if existing:
        raise HTTPException(400, "Email ya registrado")

    new_user = User(
        role_id=user.role_id,
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# GET ALL
# =========================

def get_users(db: Session):

    return db.query(User).filter(
        User.deleted_at == None
    ).all()


# =========================
# GET ONE
# =========================

def get_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    return user

#buscar usuario por correo

def get_user_by_email(db: Session, email: str):

    user = db.query(User).filter(
        User.email == email,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    return user


# =========================
# UPDATE
# =========================

def update_user(db: Session, user_id: int, data: UserUpdate):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    update_data = data.dict(exclude_unset=True)

    # Validar email duplicado
    if "email" in update_data:
        existing = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id,
            User.deleted_at == None
        ).first()

        if existing:
            raise HTTPException(400, "Email ya registrado")

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user

# login
def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(
        User.email == email,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    if not verify_password(password, user.password):
        raise HTTPException(400, "Contraseña incorrecta")

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "role_id": user.role_id,
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "gps_status": user.gps_status,
            "created_at": user.created_at
        }
    }

# =========================
# SOFT DELETE
# =========================

def delete_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    user.deleted_at = datetime.utcnow()
    user.is_active = False

    db.commit()

    return {"message": "Usuario eliminado lógicamente"}


# =========================
# RESTORE
# =========================

def restore_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at != None
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado o no está eliminado")

    user.deleted_at = None
    user.is_active = True

    db.commit()

    return {"message": "Usuario restaurado correctamente"}