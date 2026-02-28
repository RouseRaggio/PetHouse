from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.tracker_schema import TrackerResponse
from app.controllers.tracker_controller import get_adoption_history 

router = APIRouter(prefix="/tracker", tags=["Tracker"])


@router.get("/adoption/{adoption_id}", response_model=List[TrackerResponse])
def get_history(adoption_id: int, db: Session = Depends(get_db)):
    return get_adoption_history(db, adoption_id)