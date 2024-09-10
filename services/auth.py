from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from repository.user import UserRepository
from infrastructure.mysql import get_db
from schema.database.token import Token, TokenData
from datetime import timedelta, datetime
from typing import Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config.config import SECRET_KEY, ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/users/token")

class AuthService:
    def __init__(self, db:Session):
        self.user_repository = UserRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    
    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        identifier: str = payload.get("sub")
        user_id: int = payload.get("id")
        if identifier is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=identifier)
    except InvalidTokenError:
        raise credentials_exception
    user = UserRepository(db).get_user_by_username(username=token_data.username) or UserRepository(db).get_user_by_line_id(line_id=identifier)
    if user is None:
        raise credentials_exception
    return user