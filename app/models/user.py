from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    deleted_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users")

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
 