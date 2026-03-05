from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrackerLocationCreate(BaseModel):
    adoption_id: int
    latitude: float
    longitude: float
    address: Optional[str] = None


class TrackerLocationResponse(BaseModel):
    id: int
    adoption_id: int
    recorded_by: int
    latitude: float
    longitude: float
    address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True