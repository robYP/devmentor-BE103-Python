from pydantic import BaseModel


class RecordBase(BaseModel):
    action: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    user_id: int
    event_id: int

    class Config:
        orm_mode = True