from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: Optional[str] = None
    password: str
    language: str | None = "EN"
    line_user_id: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
