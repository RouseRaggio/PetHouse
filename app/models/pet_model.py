from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    publisher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    race = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String)
    description = Column(String)
    image_url = Column(String)
    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    publisher = relationship("User", back_populates="pets")
    adoptions = relationship("Adoption", back_populates="pet")
    tracker = relationship("Tracker", back_populates="pet", uselist=False)
