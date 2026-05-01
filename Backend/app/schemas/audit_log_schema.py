from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class AuditLogCreate(BaseModel):
    user_id: Optional[int]
    action: str
    resource: str
    resource_id: Optional[int] = None
    changes: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    status: str = "success"
    details: Optional[str] = None

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource: str
    resource_id: Optional[int]
    changes: Optional[Dict[str, Any]]
    timestamp: datetime
    ip_address: Optional[str]
    status: str
    details: Optional[str]

    class Config:
        from_attributes = True

class AuditLogFilter(BaseModel):
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0
