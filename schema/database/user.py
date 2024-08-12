from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    language: str | None = "en-US"


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
