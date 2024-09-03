from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.event_user import EventUserRepository
from typing import List, Dict


class TriggerService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)
        self.event_user_repository = EventUserRepository(db)


    def get_event_route(self, event_id: int):
        event = self.event_repository.search_event_by_id(event_id)
        if event:
            return event.route
        return None
    
    
    def get_event_subscribers(self, event_id: int):
        subscribers = self.event_user_repository.list_subscribers(event_id)
        if subscribers:
            users = []
            for sub in subscribers:
                users.append(sub.user_id)
            return users
        return None