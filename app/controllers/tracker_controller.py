from sqlalchemy.orm import Session
from app.models.tracker_model import Tracker


def create_tracker(
    db: Session,
    adoption_id: int,
    old_status_id: int,
    new_status_id: int,
    user_id: int
):

    tracker = Tracker(
        adoption_id=adoption_id,
        old_status_id=old_status_id,
        new_status_id=new_status_id,
        changed_by=user_id
    )

    db.add(tracker)
    db.commit()
    db.refresh(tracker)

    return tracker


def get_adoption_history(db: Session, adoption_id: int):

    return db.query(Tracker).filter(
        Tracker.adoption_id == adoption_id
    ).order_by(Tracker.created_at).all()