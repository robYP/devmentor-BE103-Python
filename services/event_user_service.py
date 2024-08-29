from sqlalchemy.orm import Session
from repository.event_user import EventUserRepository



class EventUserService:
    def __init__(self, db: Session):
        self.event_user_repository = EventUserRepository(db)
        
        
    def get_subscribers(self, event_id: int):
        return self.event_user_repository.get_subscribers(event_id=event_id)
        
        
    def subscribe(self, event_id:int, user_id:int):
        subscription = self.event_user_repository.subscribe(event_id=event_id, user_id=user_id)
        return subscription
    
    
    def unsubscribe(self, event_id:int, user_id:int):
        unsubscribed = self.event_user_repository.unsubscribe(event_id=event_id, user_id=user_id)
        return unsubscribed
    
    
    