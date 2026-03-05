from pydantic import BaseModel
from datetime import datetime


class TrackerResponse(BaseModel):
    id: int
    adoption_id: int
    old_status_id: int
    new_status_id: int
    changed_by: int
    created_at: datetime

    class Config:
        from_attributes = True