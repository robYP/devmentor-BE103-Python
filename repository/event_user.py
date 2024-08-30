from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.event_user import EventUser
from schema.database.event import EventCreate


class EventUserRepository:
    def __init__(self, db:Session):
        self.db = db
    
        
    def list_subscribers(self, event_id: int):
        return self.db.query(EventUser).filter(EventUser.event_id == event_id).all()
    
    
    def get_subscription(self, event_id:int, user_id:int):
        return self.db.query(EventUser).filter(
            EventUser.event_id == event_id,
            EventUser.user_id == user_id
        ).first()
        
    
    def create_subscription(self, event_id:int, user_id:int):
        new_subscription = EventUser(event_id=event_id, user_id=user_id)
        self.db.add(new_subscription)
        self.db.commit()
        return new_subscription
    
      
    def delete_subscription(self, subscription: EventUser):
        self.db.delete(subscription)
        self.db.commit()
        return 