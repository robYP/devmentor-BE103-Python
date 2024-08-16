from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.record import Record


def create_record(user_id: int, event_id: int, action: str, db:Session):
    db_record = Record(action=action,
                       user_id= user_id,
                       event_id=event_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record