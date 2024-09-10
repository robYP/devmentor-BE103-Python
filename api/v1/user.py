from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from infrastructure.mysql import get_db

from services.user import UserService
from database.user import User
from schema.database.user import UserCreate
from schema.database.token import Token
import jwt
from services.auth import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from config.config import LINE_CHANNEL_ID, LINE_CALLBACK_URL, LINE_CHANNEL_SECRET
import requests
from requests.exceptions import RequestException


router = APIRouter(
    tags=["user"],
    prefix="/users"
)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db=db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, 
                service: UserService = Depends(get_user_service), 
                auth_service: AuthService = Depends(get_auth_service)):
    user = User(
        username = user.username,
        password = auth_service.pwd_context.hash(user.password),
        language = user.language
    )
    return service.create_user(user=user)


@router.post("/get_users")
async def get_users(username, password, service: AuthService = Depends(get_auth_service)):
    user = service.authenticate_user(username, password)
    return user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 service: AuthService = Depends(get_auth_service)):
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username,
              "id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/currentUser")
async def read_current_user(user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}


@router.get("/line-login")
async def line_login():
    line_login_url = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={LINE_CHANNEL_ID}&redirect_uri={LINE_CALLBACK_URL}&state=12345abcde&scope=profile%20openid"
    return {"LINE login URL": line_login_url}


def get_line_access_token(code):
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINE_CALLBACK_URL,
        "client_id": LINE_CHANNEL_ID,
        "client_secret": LINE_CHANNEL_SECRET
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get access token")
    
    
def verify_token(access_token):
        verify_token_url = "https://api.line.me/oauth2/v2.1/verify"
        param = {
            "access_token":access_token,
        }
        response = requests.get(verify_token_url, params=param)
        if response.status_code == 200:
            return response.json()
        return None
    

@router.get("/callback")
async def line_callback(code: str, state: str):
    # Exchange code for access token
    print("#######################")
    print(f"code:{code}")
    print(f"state:{state}")
    token_response = get_line_access_token(code)
    if not token_response:
        raise HTTPException(status_code=400, detail="Failed to get LINE access token")
    print(f"token_response:{token_response}")
   
    token_info = verify_token(token_response["access_token"])
    if not token_info:
        raise HTTPException(status_code=400, detail="Failed to get LINE access token")
    print(f"token_info:{token_info}")
    
    return token_info