from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.event_user import EventUser
from schema.database.event import EventCreate


class EventUserRepository:
    def __init__(self, db:Session):
        self.db = db
    
        
    def get_subscribers(self, event_id: int):
        return self.db.query(EventUser).filter(EventUser.event_id == event_id).all()
        
    
    def subscribe(self, event_id:int, user_id:int):
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None 
        
        db_event_user = EventUser(event_id=event_id, user_id=user_id)
        
        subscription = self.db.query(EventUser).filter(
            EventUser.event_id == event_id,
            EventUser.user_id == user_id
        ).first()
        
        if subscription:
            return None
        
        self.db.add(db_event_user)
        self.db.commit()
        self.db.refresh(db_event_user)
        return db_event_user
    
    
    def unsubscribe(self, event_id:int, user_id:int):
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None 
        
        subscription = self.db.query(EventUser).filter(
            EventUser.event_id == event_id,
            EventUser.user_id == user_id
        ).first()
        
        if subscription:
            self.db.delete(subscription)
            self.db.commit()
            return subscription
        
        return subscription