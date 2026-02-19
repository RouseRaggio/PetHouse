from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password




def create_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(
        User.email == user.email,
        User.deleted_at == None
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = User(
        nombre=user.nombre,
        email=user.email,
        password=hash_password(user.password),
        role_id=user.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users(db: Session):
    return db.query(User).filter(
        User.deleted_at == None
    ).all()




def get_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user




def update_user(db: Session, user_id: int, user_data: UserUpdate):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar email duplicado si cambia
    if user_data.email and user_data.email != user.email:
        existing_email = db.query(User).filter(
            User.email == user_data.email,
            User.deleted_at == None
        ).first()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        user.email = user_data.email

    if user_data.nombre:
        user.nombre = user_data.nombre

    if user_data.password:
        user.password = hash_password(user_data.password)

    if user_data.role_id:
        user.role_id = user_data.role_id

    db.commit()
    db.refresh(user)

    return user



def delete_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Usuario eliminado lógicamente"}




def restore_user(db: Session, user_id: int):

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at != None
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no está eliminado")

    user.deleted_at = None
    db.commit()

    return {"message": "Usuario restaurado correctamente"}
