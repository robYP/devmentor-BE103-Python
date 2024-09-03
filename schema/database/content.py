from pydantic import BaseModel


class ContentBase(BaseModel):
    content: str
    event_id: int
    language: str


class ContentCreate(ContentBase):
    pass


class Content(ContentBase):
    id: int
        
    class Config:
        orm_mode = True