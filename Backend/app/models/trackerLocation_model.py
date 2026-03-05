from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class TrackerLocation(Base):
    __tablename__ = "tracker_locations"

    id = Column(Integer, primary_key=True)

    adoption_id = Column(Integer, ForeignKey("adoptions.id"))
    recorded_by = Column(Integer, ForeignKey("users.id"))

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    address = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    adoption = relationship("Adoption")
    user = relationship("User")