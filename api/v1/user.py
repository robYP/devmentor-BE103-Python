from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from infrastructure.mysql import get_db

import repository.user
from database.user import User
from schema.database.user import UserCreate
from schema.database.token import Token
import jwt
from services.auth import pwd_context, authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    tags=["user"],
    prefix="/users"
)


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


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,
              "id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/currentUser")
async def read_current_user(user: Annotated[dict, Depends(get_current_user)], db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}