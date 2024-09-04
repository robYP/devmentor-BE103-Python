from pydantic import BaseModel
from datetime import datetime


class EventUserBase(BaseModel):
    event_id: int
    user_id: int
    notify_time: datetime

class EventUserCreate(EventUserBase):
    pass
    

class EventUser(EventUserBase):
    id: int
    
    class Config:
        orm_mode = True