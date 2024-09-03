from sqlalchemy.orm import Session
from repository.user import UserRepository
from schema.database.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db=db)
        self.db = db
        

    def create_user(self, user: UserCreate):
        new_user = self.user_repository.create(user=user)
        return new_user


    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        return user