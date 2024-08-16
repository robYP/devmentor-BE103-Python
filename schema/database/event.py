from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    name: str
    route: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    creator_id: int
    create_time: Optional[datetime] = None
    
    class Config:
        orm_mode = True