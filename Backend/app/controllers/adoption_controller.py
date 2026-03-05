from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.adoption_model import Adoption
from app.models.pet_model import Pet
from app.models.adoption_status_model import AdoptionStatus


# =========================
# CREATE ADOPTION
# =========================

def create_adoption(db: Session, data, user_id: int):

    pet = db.query(Pet).filter(
        Pet.id == data.pet_id,
        Pet.deleted_at == None
    ).first()

    if not pet:
        raise HTTPException(404, "Mascota no encontrada")

    # Validar que no esté adoptado
    approved_status = db.query(AdoptionStatus).filter(
        AdoptionStatus.name == "APPROVED"
    ).first()

    existing_approved = db.query(Adoption).filter(
        Adoption.pet_id == data.pet_id,
        Adoption.status_id == approved_status.id,
        Adoption.deleted_at == None
    ).first()

    if existing_approved:
        raise HTTPException(400, "La mascota ya fue adoptada")

    adoption = Adoption(
        pet_id=data.pet_id,
        adoptante_id=user_id,
        status_id=1,  # PENDING
        quiere_tracker=data.quiere_tracker,
        cedula_url=data.cedula_url,
        recibo_url=data.recibo_url
    )

    db.add(adoption)
    db.commit()
    db.refresh(adoption)

    return adoption


# =========================
# GET ALL
# =========================

def get_adoptions(db: Session):

    return db.query(Adoption).filter(
        Adoption.deleted_at == None
    ).all()


# =========================
# GET ONE
# =========================

def get_adoption(db: Session, adoption_id: int):

    adoption = db.query(Adoption).filter(
        Adoption.id == adoption_id,
        Adoption.deleted_at == None
    ).first()

    if not adoption:
        raise HTTPException(404, "Adopción no encontrada")

    return adoption


# =========================
# CHANGE STATUS
# =========================

def change_adoption_status(db: Session, adoption_id: int, status_id: int):

    adoption = db.query(Adoption).filter(
        Adoption.id == adoption_id,
        Adoption.deleted_at == None
    ).first()

    if not adoption:
        raise HTTPException(404, "Adopción no encontrada")

    status = db.query(AdoptionStatus).filter(
        AdoptionStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(404, "Estado inválido")

    # Validar estado final
    current_status = db.query(AdoptionStatus).filter(
        AdoptionStatus.id == adoption.status_id
    ).first()

    if current_status.is_final:
        raise HTTPException(400, "Esta adopción ya es final")

    adoption.status_id = status_id
    adoption.fecha_respuesta = datetime.utcnow()

    db.commit()
    db.refresh(adoption)

    return adoption


# =========================
# SOFT DELETE
# =========================

def delete_adoption(db: Session, adoption_id: int):

    adoption = db.query(Adoption).filter(
        Adoption.id == adoption_id,
        Adoption.deleted_at == None
    ).first()

    if not adoption:
        raise HTTPException(404, "Adopción no encontrada")

    adoption.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Adopción eliminada lógicamente"}