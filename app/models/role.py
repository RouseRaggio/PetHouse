# app/models/role.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relación con usuarios
    users = relationship("User", back_populates="role")

    # Relación muchos a muchos con permisos
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )
