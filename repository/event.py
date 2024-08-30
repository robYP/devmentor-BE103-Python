from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.event_user import EventUser
from schema.database.event import EventCreate


class EventRepository:
    def __init__(self, db:Session):
        self.db = db


    def search_event_by_id(self, event_id:int):
        db_event = self.db.query(Event).filter(Event.id == event_id).first()
        if not db_event:
            return None
        return db_event


    def get_events(self, skip: int = 0, limit: int = 100):
        return self.db.query(Event).offset(skip).limit(limit).all()


    def create_event(self, user: User, event: EventCreate):
        db_event = Event(name = event.name,
                         route= event.route,
                         creator_id = user.id)
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event


    def delete_event_by_id(self, event_id:int):
        db_event = self.search_event_by_id(event_id=event_id)
        if db_event == None:
            return None
        self.db.delete(db_event)
        self.db.commit()
        return db_event


    def update_event_by_id(self, event_id: int, event: EventCreate):
        db_event = self.search_event_by_id(event_id=event_id)
        if db_event == None:
            return None
        db_event.name = event.name
        db_event.route= event.route
        self.db.commit()
        self.db.refresh(db_event)
        return db_event