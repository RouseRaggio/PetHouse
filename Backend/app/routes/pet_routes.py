from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.pet_schema import PetCreate, PetUpdate, PetResponse
from app.controllers.pet_controller import (
    create_pet,
    get_pets,
    get_pet,
    update_pet,
    delete_pet
)
from app.controllers.pet_health_controller import get_user_pets
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/pets", tags=["Pets"])


def parse_birth_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise HTTPException(status_code=422, detail="Formato de fecha inválido. Use YYYY-MM-DD o DD/MM/YYYY.")


def _format_pet_image_url(pet, request: Request):
    if not pet:
        return
    if pet.image_url and pet.image_url.startswith("data:"):
        base_url = str(request.base_url).rstrip('/')
        pet.image_url = f"{base_url}/pets/{pet.id}/image"


def _format_pets_image_url(pets, request: Request):
    for pet in pets:
        _format_pet_image_url(pet, request)


# CREATE
@router.post("", response_model=PetResponse)
def create(
    request: Request,
    name: str = Form(...),
    species: str = Form(...),
    race: Optional[str] = Form(None),
    birth_date: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    modalidad: Optional[str] = Form("sede"),
    telefono_contacto: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    pet_data = PetCreate(
        name=name,
        species=species,
        race=race,
        birth_date=parse_birth_date(birth_date) if birth_date else None,
        gender=gender,
        description=description,
        image_url=None,
        modalidad=modalidad,
        telefono_contacto=telefono_contacto,
    )
    pet = create_pet(db, pet_data, user_id=current_user.id, image=image)
    _format_pet_image_url(pet, request)
    return pet


# GET ALL
@router.get("", response_model=List[PetResponse])
def read_all(request: Request, status: Optional[str] = None, db: Session = Depends(get_db)):
    pets = get_pets(db, status=status)
    _format_pets_image_url(pets, request)
    return pets


# GET MY PETS
# Esta ruta debe declararse antes de /{pet_id} para evitar que "my" se intente parsear como int.
@router.get("/my", response_model=List[PetResponse])
def read_my_pets(request: Request, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    pets = get_user_pets(db, current_user.id)
    _format_pets_image_url(pets, request)
    return pets


# GET ONE IMAGE
@router.get("/{pet_id}/image")
def read_pet_image(pet_id: int, db: Session = Depends(get_db)):
    pet = get_pet(db, pet_id)
    if not pet or not pet.image_data:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return Response(content=pet.image_data, media_type="image/jpeg")


# GET ONE
@router.get("/{pet_id}", response_model=PetResponse)
def read_one(pet_id: int, request: Request, db: Session = Depends(get_db)):
    pet = get_pet(db, pet_id)
    _format_pet_image_url(pet, request)
    return pet


# UPDATE
@router.put("/{pet_id}", response_model=PetResponse)
def update(pet_id: int, request: Request, data: PetUpdate, db: Session = Depends(get_db)):
    pet = update_pet(db, pet_id, data)
    _format_pet_image_url(pet, request)
    return pet


# DELETE (Soft)
@router.delete("/{pet_id}")
def delete(pet_id: int, db: Session = Depends(get_db)):
    return delete_pet(db, pet_id)


# SEND SEDE INSTRUCTIONS EMAIL (without approving)
@router.post("/{pet_id}/send-instructions")
def send_instructions(pet_id: int, db: Session = Depends(get_db)):
    from app.controllers.pet_controller import get_pet
    from app.core.email import send_sede_instructions_email
    pet = get_pet(db, pet_id)
    if not pet.publisher:
        raise HTTPException(400, "El publicador no tiene correo registrado")
    sent = send_sede_instructions_email(pet.publisher.email, pet.publisher.name, pet.name)
    if not sent:
        raise HTTPException(500, "No se pudo enviar el correo. Verifica las credenciales SMTP.")
    return {"message": f"Instrucciones enviadas a {pet.publisher.email}"}