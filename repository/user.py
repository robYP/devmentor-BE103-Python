from sqlalchemy.orm import Session

from database.user import User
from schema.database.user import UserCreate

def create(db: Session, user: User):
    db_user = user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user