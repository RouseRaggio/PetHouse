from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True)

    adoption_id = Column(Integer, ForeignKey("adoptions.id"))
    old_status_id = Column(Integer, ForeignKey("adoption_status.id"))
    new_status_id = Column(Integer, ForeignKey("adoption_status.id"))
    changed_by = Column(Integer, ForeignKey("users.id"))
    pet_id = Column(Integer, ForeignKey("pets.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    adoption = relationship("Adoption")
    old_status = relationship("AdoptionStatus", foreign_keys=[old_status_id])
    new_status = relationship("AdoptionStatus", foreign_keys=[new_status_id])
    user = relationship("User")
    pet = relationship("Pet", back_populates="tracker")