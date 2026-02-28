from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.adoption_schema import (
    AdoptionCreate,
    AdoptionStatusUpdate,
    AdoptionResponse
)
from app.controllers.adoption_controller import (
    create_adoption,
    get_adoptions,
    get_adoption,
    change_adoption_status,
    delete_adoption
)

router = APIRouter(prefix="/adoptions", tags=["Adoptions"])


@router.post("/", response_model=AdoptionResponse)
def create(data: AdoptionCreate, db: Session = Depends(get_db)):
    # Luego conectaremos JWT
    return create_adoption(db, data, user_id=1)


@router.get("/", response_model=List[AdoptionResponse])
def read_all(db: Session = Depends(get_db)):
    return get_adoptions(db)


@router.get("/{adoption_id}", response_model=AdoptionResponse)
def read_one(adoption_id: int, db: Session = Depends(get_db)):
    return get_adoption(db, adoption_id)


@router.put("/{adoption_id}/status", response_model=AdoptionResponse)
def change_status(adoption_id: int, data: AdoptionStatusUpdate, db: Session = Depends(get_db)):
    return change_adoption_status(db, adoption_id, data.status_id)


@router.delete("/{adoption_id}")
def delete(adoption_id: int, db: Session = Depends(get_db)):
    return delete_adoption(db, adoption_id)