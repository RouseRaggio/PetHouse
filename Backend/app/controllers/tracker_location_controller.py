from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.trackerLocation_model import TrackerLocation
from app.models.adoption_model import Adoption


def create_tracker_location(
    db: Session,
    data,
    user_id: int
):

    adoption = db.query(Adoption).filter(
        Adoption.id == data.adoption_id
    ).first()

    if not adoption:
        raise HTTPException(404, "Adopción no encontrada")

    location = TrackerLocation(
        adoption_id=data.adoption_id,
        recorded_by=user_id,
        latitude=data.latitude,
        longitude=data.longitude,
        address=data.address
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def get_adoption_locations(db: Session, adoption_id: int):

    return db.query(TrackerLocation).filter(
        TrackerLocation.adoption_id == adoption_id
    ).order_by(TrackerLocation.created_at).all()