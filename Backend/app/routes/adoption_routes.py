import base64
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.adoption_schema import (
    AdoptionCreate,
    AdoptionStatusUpdate,
    AdoptionResponse
)
from app.auth.dependencies import get_current_active_user
from app.controllers.adoption_controller import (
    create_adoption,
    get_adoptions,
    get_adoption,
    change_adoption_status,
    delete_adoption
)

router = APIRouter(prefix="/adoptions", tags=["Adoptions"])


def _upload_file_to_data_uri(file: UploadFile):
    contents = file.file.read()
    mime = file.content_type or "application/octet-stream"
    encoded = base64.b64encode(contents).decode("utf-8")
    return f"data:{mime};base64,{encoded}"
    


@router.post("/", response_model=AdoptionResponse)
def create(
    pet_id: int = Form(...),
    quiere_tracker: bool = Form(False),
    cedula: Optional[UploadFile] = File(None),
    recibo: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cedula_url = _upload_file_to_data_uri(cedula) if cedula else None
    recibo_url = _upload_file_to_data_uri(recibo) if recibo else None

    data = AdoptionCreate(
        pet_id=pet_id,
        quiere_tracker=quiere_tracker,
        cedula_url=cedula_url,
        recibo_url=recibo_url
    )
    return create_adoption(db, data, user_id=current_user.id)


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

