from sqlalchemy.orm import Session
from database.user import User


class UserRepository:
    def __init__(self, db:Session):
        self.db = db
    
    
    def create(self, user: User):
        db_user = user
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def get_user_by_username(self, username:str):
        return self.db.query(User).filter(User.username == username).first()
    
    
    def get_user_by_user_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    
    def get_users_by_user_ids(self, user_ids: list[int]):
        return self.db.query(User).filter(User.id.in_(user_ids)).all()
    
    
    def get_user_by_line_id(self, line_id: str):
        return self.db.query(User).filter(User.line_user_id == line_id).first()