from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password
from app.core.security import verify_password
from app.auth.jwt_handler import create_access_token
from app.core.email import send_gps_email
from app.controllers.audit_log_controller import log_action


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

    try:
        log_action(
            db=db,
            user_id=None,
            action="create",
            resource="user",
            resource_id=new_user.id,
            changes=user.dict(exclude={"password"}),
            status="success"
        )
    except Exception as e:
        print(f"Audit logging error: {e}")

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

    try:
        log_action(
            db=db,
            user_id=None,
            action="update",
            resource="user",
            resource_id=user.id,
            changes=update_data,
            status="success"
        )
    except Exception as e:
        print(f"Audit logging error: {e}")

    # Envío de correo real si el GPS es aprobado O si se actualiza el IMEI de un usuario ya aprobado
    is_becoming_approved = ("gps_status" in update_data and update_data["gps_status"] == "approved")
    is_updating_imei = ("gps_imei" in update_data and user.gps_status == "approved")

    if is_becoming_approved or is_updating_imei:
        print(f"--- Iniciando proceso de envío de correo a {user.email} ---")
        send_gps_email(user.email, user.name, user.gps_imei)

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

    try:
        log_action(
            db=db,
            user_id=user.id,
            action="login",
            resource="user",
            resource_id=user.id,
            details="Login exitoso",
            status="success"
        )
    except Exception as e:
        print(f"Audit logging error: {e}")

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
            "gps_imei": user.gps_imei,
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

    try:
        log_action(
            db=db,
            user_id=None,
            action="delete",
            resource="user",
            resource_id=user.id,
            details=f"Usuario {user.email} eliminado",
            status="success"
        )
    except Exception as e:
        print(f"Audit logging error: {e}")

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

    try:
        log_action(
            db=db,
            user_id=None,
            action="restore",
            resource="user",
            resource_id=user.id,
            details=f"Usuario {user.email} restaurado",
            status="success"
        )
    except Exception as e:
        print(f"Audit logging error: {e}")

    return {"message": "Usuario restaurado correctamente"}