from sqlalchemy.orm import Session
from repository.event_user import EventUserRepository
from repository.event import EventRepository


class EventUserService:
    def __init__(self, db: Session):
        self.event_user_repository = EventUserRepository(db=db)
        self.event_repository = EventRepository(db=db)
        
        
    def list_subscribers(self, event_id: int):
        return self.event_user_repository.list_subscribers(event_id=event_id)
        
        
    def subscribe(self, event_id:int, user_id:int):
        event = self.event_repository.search_event_by_id(event_id)
        if not event: 
            return None
        
        subscription = self.event_user_repository.get_subscription(event_id=event_id, user_id=user_id)
        if subscription:
            return None
        
        new_subscription = self.event_user_repository.create_subscription(event_id=event_id, user_id=user_id)
        return new_subscription
    
    
    def unsubscribe(self, event_id:int, user_id:int):
        event = self.event_repository.search_event_by_id(event_id)
        if not event:
            return None
        
        subscription = self.event_user_repository.get_subscription(event_id=event_id, user_id=user_id)
        if not subscription:
            return None
        
        self.event_user_repository.delete_subscription(subscription)
        return subscription
    
    
    