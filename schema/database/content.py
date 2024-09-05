from pydantic import BaseModel
from schema.database.language import Language


class ContentBase(BaseModel):
    content: str


class ContentCreate(ContentBase):
    pass


class Content(ContentBase):
    id: int
    event_id: int
    language: Language
        
    class Config:
        orm_mode = True