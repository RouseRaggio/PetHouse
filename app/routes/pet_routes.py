from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.pet_schema import PetCreate, PetUpdate, PetResponse
from app.controllers.pet_controller import (
    create_pet,
    get_pets,
    get_pet,
    update_pet,
    delete_pet
)

router = APIRouter(prefix="/pets", tags=["Pets"])


# CREATE
@router.post("/", response_model=PetResponse)
def create(pet: PetCreate, db: Session = Depends(get_db)):
    # Aquí luego conectaremos el usuario autenticado
    return create_pet(db, pet, user_id=1)


# GET ALL
@router.get("/", response_model=List[PetResponse])
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