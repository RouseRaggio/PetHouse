from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
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


# CREATE
@router.post("", response_model=PetResponse)
def create(
    name: str = Form(...),
    species: str = Form(...),
    race: Optional[str] = Form(None),
    birth_date: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Aquí luego conectaremos el usuario autenticado
    pet_data = PetCreate(
        name=name,
        species=species,
        race=race,
        birth_date=parse_birth_date(birth_date) if birth_date else None,
        gender=gender,
        description=description,
        image_url=None  # Se asignará si hay imagen
    )
    return create_pet(db, pet_data, user_id=current_user.id, image=image)


# GET ALL
@router.get("", response_model=List[PetResponse])
def read_all(db: Session = Depends(get_db)):
    return get_pets(db)


# GET ONE
@router.get("/{pet_id}", response_model=PetResponse)
def read_one(pet_id: int, db: Session = Depends(get_db)):
    return get_pet(db, pet_id)


# UPDATE
@router.put("/{pet_id}", response_model=PetResponse)
def update(pet_id: int, data: PetUpdate, db: Session = Depends(get_db)):
    return update_pet(db, pet_id, data)


# DELETE (Soft)
@router.delete("/{pet_id}")
def delete(pet_id: int, db: Session = Depends(get_db)):
    return delete_pet(db, pet_id)