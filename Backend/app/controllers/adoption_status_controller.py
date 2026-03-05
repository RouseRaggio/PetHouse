from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.adoption_status_model import AdoptionStatus


# =========================
# CREATE
# =========================

def create_adoption_status(db: Session, data):

    existing = db.query(AdoptionStatus).filter(
        AdoptionStatus.name == data.name
    ).first()

    if existing:
        raise HTTPException(400, "Este estado ya existe")

    status = AdoptionStatus(
        name=data.name.upper(),
        is_final=data.is_final,
        order=data.order
    )

    db.add(status)
    db.commit()
    db.refresh(status)

    return status


# =========================
# GET ALL
# =========================

def get_adoption_statuses(db: Session):

    return db.query(AdoptionStatus).order_by(
        AdoptionStatus.order
    ).all()


# =========================
# GET ONE
# =========================

def get_adoption_status(db: Session, status_id: int):

    status = db.query(AdoptionStatus).filter(
        AdoptionStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(404, "Estado no encontrado")

    return status


# =========================
# UPDATE
# =========================

def update_adoption_status(db: Session, status_id: int, data):

    status = db.query(AdoptionStatus).filter(
        AdoptionStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(404, "Estado no encontrado")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(status, key, value)

    db.commit()
    db.refresh(status)

    return status


# =========================
# DELETE (Opcional)
# =========================

def delete_adoption_status(db: Session, status_id: int):

    status = db.query(AdoptionStatus).filter(
        AdoptionStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(404, "Estado no encontrado")

    db.delete(status)
    db.commit()

    return {"message": "Estado eliminado"}