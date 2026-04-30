from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from datetime import datetime
import base64

from app.models.pet_model import Pet
from app.models.adoption_model import Adoption
from app.models.user_model import User
from app.schemas.pet_schema import PetCreate, PetUpdate
from app.core.email import send_gps_email


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
    new_pet.adopter_name = None
    return new_pet


# =========================
# GET ALL
# =========================

def get_pets(db: Session):

    pets = db.query(Pet).filter(
        Pet.deleted_at == None
    ).all()

    for pet in pets:
        adoption = db.query(Adoption).filter(
            Adoption.pet_id == pet.id,
            Adoption.deleted_at == None
        ).order_by(Adoption.fecha_solicitud.desc()).first()
        if adoption and adoption.adoptante:
            pet.adopter_name = f"{adoption.adoptante.name} {adoption.adoptante.last_name}"
            pet.adopter_id = adoption.adoptante.id
        else:
            pet.adopter_name = None
            pet.adopter_id = None
    
    return pets


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

    adoption = db.query(Adoption).filter(
        Adoption.pet_id == pet.id,
        Adoption.deleted_at == None
    ).order_by(Adoption.fecha_solicitud.desc()).first()
    if adoption and adoption.adoptante:
        pet.adopter_name = f"{adoption.adoptante.name} {adoption.adoptante.last_name}"
        pet.adopter_id = adoption.adoptante.id
    else:
        pet.adopter_name = None
        pet.adopter_id = None

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

    # Si la mascota vuelve a estar disponible, desvincularla del adoptante anterior
    if "status" in update_data and update_data["status"] == "AVAILABLE":
        db.query(Adoption).filter(
            Adoption.pet_id == pet.id,
            Adoption.deleted_at == None
        ).update({"deleted_at": datetime.utcnow()}, synchronize_session=False)
        
        # Resetear estado GPS
        pet.gps_status = "none"
        pet.gps_imei = None

    # Envío de correo si el GPS es aprobado o se actualiza el IMEI
    is_becoming_approved = ("gps_status" in update_data and update_data["gps_status"] == "approved")
    is_updating_imei = ("gps_imei" in update_data and pet.gps_status == "approved")

    if is_becoming_approved or is_updating_imei:
        # Buscar al adoptante para enviarle el correo
        adoption = db.query(Adoption).filter(
            Adoption.pet_id == pet.id,
            Adoption.deleted_at == None
        ).order_by(Adoption.fecha_solicitud.desc()).first()

        if adoption and adoption.adoptante:
            print(f"--- Iniciando proceso de envío de correo GPS a {adoption.adoptante.email} ---")
            send_gps_email(adoption.adoptante.email, adoption.adoptante.name, pet.gps_imei)

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