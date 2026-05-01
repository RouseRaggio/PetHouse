from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import json

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)  # "create", "update", "delete", "login", "login_failed"
    resource = Column(String(50), nullable=False)  # "user", "pet", "adoption", "tracker", etc
    resource_id = Column(Integer, nullable=True)  # ID of the affected resource
    
    changes = Column(Text, nullable=True)  # JSON with before/after values
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ip_address = Column(String(45), nullable=True)
    status = Column(String(20), default="success")  # "success", "failure"
    details = Column(Text, nullable=True)  # Additional info (error messages, etc)
    
    user = relationship("User", foreign_keys=[user_id])

    def set_changes(self, changes_dict):
        """Helper to set changes as JSON"""
        if changes_dict:
            self.changes = json.dumps(changes_dict, default=str)

    def get_changes(self):
        """Helper to get changes as dict"""
        if self.changes:
            return json.loads(self.changes)
        return None
