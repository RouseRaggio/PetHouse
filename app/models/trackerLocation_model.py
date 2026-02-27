from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class TrackerLocation(Base):
    __tablename__ = "tracker_locations"

    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey("trackers.id"), nullable=False)

    latitud = Column(DECIMAL(9,6), nullable=False)
    longitud = Column(DECIMAL(9,6), nullable=False)

    fecha_registro = Column(DateTime, default=datetime.utcnow)

    tracker = relationship("Tracker", back_populates="locations")