from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.tracker_location_schema import (
    TrackerLocationCreate,
    TrackerLocationResponse
)
from app.controllers.tracker_location_controller import (
    create_tracker_location,
    get_adoption_locations
)

router = APIRouter(prefix="/tracker-location", tags=["Tracker Location"])


@router.post("/", response_model=TrackerLocationResponse)
def create_location(
    data: TrackerLocationCreate,
    db: Session = Depends(get_db)
):
    # aquí luego conectamos con current_user
    return create_tracker_location(db, data, user_id=1)


@router.get("/adoption/{adoption_id}", response_model=List[TrackerLocationResponse])
def get_locations(
    adoption_id: int,
    db: Session = Depends(get_db)
):
    return get_adoption_locations(db, adoption_id)