from pydantic import BaseModel
from datetime import datetime


class RecordBase(BaseModel):
    action: str
    event_name: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    user_id: int
    event_id: int
    created_at: datetime

    class Config:
        orm_mode = True