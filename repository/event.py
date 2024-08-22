from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from schema.database.event import EventCreate


def search_event_by_id(db:Session, event_id:int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()


def create_event(user: User, event: EventCreate, db: Session):
    db_event = Event(name = event.name, 
                     route= event.route,  
                     creator_id = user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event_by_id(db:Session, event_id:int):
    db_event = search_event_by_id(db=db, event_id=event_id)
    if db_event == None:
        return None
    db.delete(db_event)
    db.commit()
    return db_event


def update_event_by_id(user: User, event_id: int, event: EventCreate, db: Session):
    db_event = search_event_by_id(db=db, event_id=event_id)
    if db_event == None:
        return None
    db_event.name = event.name 
    db_event.route= event.route
    db.commit()
    db.refresh(db_event)
    return db_event