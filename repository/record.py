from sqlalchemy.orm import Session
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
    
    
    def create_triggered_record(self, action: str, event_id: int):
        db_record = Record(action=action,
                           user_id=None,
                           event_id=event_id)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record
    
    
    def list_records(self, skip: int=0, limit: int= 100 ):
        return self.db.query(Record).offset(skip).limit(limit).all()