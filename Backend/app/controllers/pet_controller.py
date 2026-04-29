from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from datetime import datetime
import base64

from app.models.pet_model import Pet
from app.schemas.pet_schema import PetCreate, PetUpdate


# =========================
# CREATE
# =========================

def _upload_file_to_data_uri(file: UploadFile):
    contents = file.file.read()
    mime = file.content_type or "application/octet-stream"
    encoded = base64.b64encode(contents).decode("utf-8")
    return f"data:{mime};base64,{encoded}", contents


def create_pet(db: Session, pet: PetCreate, user_id: int, image: UploadFile = None):
    image_url = None
    image_data = None
    if image:
        image_url, image_data = _upload_file_to_data_uri(image)

    new_pet = Pet(
        publisher_id=user_id,
        name=pet.name,
        species=pet.species,
        race=pet.race,
        birth_date=pet.birth_date,
        gender=pet.gender,
        description=pet.description,
        image_url=image_url,
        image_data=image_data,
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