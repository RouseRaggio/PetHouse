from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Adoption(Base):
    __tablename__ = "adoptions"

    id = Column(Integer, primary_key=True)

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    adoptante_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("adoption_status_model.id"), nullable=False)

    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_respuesta = Column(DateTime)

    cedula_url = Column(String)
    recibo_url = Column(String)

    quiere_tracker = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    pet = relationship("Pet", back_populates="adoptions")
    status = relationship("AdoptionStatus")
    adoptante = relationship("User")