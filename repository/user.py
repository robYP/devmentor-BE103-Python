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