from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class AdoptionStatus(Base):
    __tablename__ = "adoption_status"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    is_final = Column(Boolean, default=False)
    order = Column(Integer, nullable=False)