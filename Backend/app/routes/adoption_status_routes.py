from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.adoption_status_schema import (
    AdoptionStatusCreate,
    AdoptionStatusUpdate,
    AdoptionStatusResponse
)
from app.controllers.adoption_status_controller import (
    create_adoption_status,
    get_adoption_statuses,
    get_adoption_status,
    update_adoption_status,
    delete_adoption_status
)

router = APIRouter(prefix="/adoption-status", tags=["Adoption Status"])


@router.post("/", response_model=AdoptionStatusResponse)
def create(data: AdoptionStatusCreate, db: Session = Depends(get_db)):
    return create_adoption_status(db, data)


@router.get("/", response_model=List[AdoptionStatusResponse])
def read_all(db: Session = Depends(get_db)):
    return get_adoption_statuses(db)


@router.get("/{status_id}", response_model=AdoptionStatusResponse)
def read_one(status_id: int, db: Session = Depends(get_db)):
    return get_adoption_status(db, status_id)


@router.put("/{status_id}", response_model=AdoptionStatusResponse)
def update(status_id: int, data: AdoptionStatusUpdate, db: Session = Depends(get_db)):
    return update_adoption_status(db, status_id, data)


@router.delete("/{status_id}")
def delete(status_id: int, db: Session = Depends(get_db)):
    return delete_adoption_status(db, status_id)