from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.event_user import EventUserRepository
from repository.content import ContentRepository
from repository.user import UserRepository
from typing import Optional


class TriggerService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)
        self.event_user_repository = EventUserRepository(db)
        self.content_repository = ContentRepository(db)
        self.user_repository = UserRepository(db)


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
    
    
    def get_event_content(self, event_id: int, user_id: int) -> Optional[str]:
        user = self.user_repository.get_user_by_user_id(user_id)
        if not user:
            return None

        subscription = self.event_user_repository.get_subscription(event_id=event_id, user_id=user.id)
        if not subscription:
            return None

        content = self.content_repository.get_content(event_id=event_id, language=user.language)
        return content.content if content else None