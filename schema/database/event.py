from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    name: str
    route: str


class EventCreate(EventBase):
    create_time: Optional[datetime] = None
    creator_id: int


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True