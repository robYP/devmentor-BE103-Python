from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repository.user import UserRepository
from schema.database.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db=db)
        self.db = db
        

    def create_user(self, user: UserCreate):
        try:
            if not user.line_user_id and not user.email:
                raise HTTPException(status_code=400, detail="Email is required for non-social login")
            
            new_user = self.user_repository.create(user=user)
            return new_user
        except IntegrityError as e:
            self.db.rollback()
            if "Duplicate entry" in str(e) and "username" in str(e):
                raise HTTPException(status_code=400, detail="Username already exists")
            elif "Duplicate entry" in str(e) and "email" in str(e):
                raise HTTPException(status_code=400, detail="Email already exists")
            else:
                raise HTTPException(status_code=400, detail="An error occurred while creating the user")


    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        return user
    
    
    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_user_id(user_id)
        return user