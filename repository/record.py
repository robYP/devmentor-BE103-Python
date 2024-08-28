from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.record import Record

class RecordRepository():
    def __init__(self, db: Session):
        self.db = db
        
        
    def create_record(self, action: str, user_id: int, event_id: int):
        db_record = Record(action=action,
                           user_id= user_id,
                           event_id=event_id)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record
    
# def create_record(user_id: int, event_id: int, action: str, db:Session):
#     db_record = Record(action=action,
#                        user_id= user_id,
#                        event_id=event_id)
#     db.add(db_record)
#     db.commit()
#     db.refresh(db_record)
#     return db_record