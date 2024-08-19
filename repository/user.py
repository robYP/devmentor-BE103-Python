from sqlalchemy.orm import Session

from database.user import User

def create(db: Session, user: User):
    db_user = user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username:str):
    return db.query(User).filter(User.username == username).first()