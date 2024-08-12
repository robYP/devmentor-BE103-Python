from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import repository.user
from infrastructure.mysql import get_db
from database.user import User
from schema.database.user import UserCreate
#-------------------
from datetime import timedelta, datetime
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


router = APIRouter(
    tags=["user"],
    prefix="/users"
)


SECRET_KEY = "b2444842593cb2648af8df3a556196a74e055cc82ea19579dcf59372a1d4a401"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username = user.username,
        password = pwd_context.hash(user.password),
        language = user.language
    )
    return repository.user.create(db=db, user=user)



# @router.get("/", status_code=status.HTTP_200_OK)
# async def get_users(user:None, db: Session = Depends(get_db)):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
#     return {"User":user}


