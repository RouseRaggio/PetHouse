from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.pet_model import Pet
from app.schemas.pet_schema import PetCreate, PetUpdate


# =========================
# CREATE
# =========================

def create_pet(db: Session, pet: PetCreate, user_id: int):

    new_pet = Pet(
        publisher_id=user_id,
        name=pet.name,
        species=pet.species,
        race=pet.race,
        birth_date=pet.birth_date,
        gender=pet.gender,
        description=pet.description,
        image_url=pet.image_url,
        status="AVAILABLE"
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet


# =========================
# GET ALL
# =========================

def get_pets(db: Session):

    return db.query(Pet).filter(
        Pet.deleted_at == None
    ).all()


# =========================
# GET ONE
# =========================

def get_pet(db: Session, pet_id: int):

    pet = db.query(Pet).filter(
        Pet.id == pet_id,
        Pet.deleted_at == None
    ).first()

    if not pet:
        raise HTTPException(404, "Mascota no encontrada")

    return pet


# =========================
# UPDATE
# =========================

def update_pet(db: Session, pet_id: int, data: PetUpdate):

    pet = db.query(Pet).filter(
        Pet.id == pet_id,
        Pet.deleted_at == None
    ).first()

    if not pet:
        raise HTTPException(404, "Mascota no encontrada")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(pet, key, value)

    db.commit()
    db.refresh(pet)

    return pet


# =========================
# SOFT DELETE
# =========================

def delete_pet(db: Session, pet_id: int):

    pet = db.query(Pet).filter(
        Pet.id == pet_id,
        Pet.deleted_at == None
    ).first()

    if not pet:
        raise HTTPException(404, "Mascota no encontrada")

    pet.deleted_at = datetime.utcnow()
    db.commit()

    return {"message": "Mascota eliminada lógicamente"}