from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.content import ContentRepository
from repository.record import RecordRepository
from schema.database.content import ContentCreate
from schema.database.language import Language

class RecordService:
    def __init__(self, db: Session):
        self.record_repository = RecordRepository(db)
        
    
    def list_records(self, skip: int=0, limit:int=100):
        records = self.record_repository.list_records(skip=skip, limit=limit)
        return records

