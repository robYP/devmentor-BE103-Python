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
        return
    
    
    def unsubscribe(self, event_id:int, user_id:int):
        return