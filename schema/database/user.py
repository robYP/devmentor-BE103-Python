from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: Optional[str] = None
    password: str
    language: str | None = "EN"
    line_user_id: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
