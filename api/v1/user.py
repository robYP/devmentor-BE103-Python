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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class UserInDB(User):
    pass

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str, db):
    user = repository.user.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username = user.username,
        password = pwd_context.hash(user.password),
        language = user.language
    )
    return repository.user.create(db=db, user=user)


@router.post("/get_users")
async def get_users(username, password, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    
    return user


