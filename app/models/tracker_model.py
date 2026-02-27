from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    serial = Column(String, unique=True, nullable=False)
    status = Column(String)

    pet = relationship("Pet", back_populates="tracker")
    locations = relationship("TrackerLocation", back_populates="tracker")