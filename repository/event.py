from sqlalchemy.orm import Session

from database.event import Event
from schema.database.event import EventCreate

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()

def create_event(event: EventCreate, db: Session):
    db_event = Event(name = event.name, 
                     route= event.route,  
                     creator_id = event.creator_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event