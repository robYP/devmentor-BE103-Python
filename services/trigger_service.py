from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.event_user import EventUserRepository
from repository.content import ContentRepository
from repository.user import UserRepository
from typing import Optional, List, Dict
from services.email_service import EmailService 


class TriggerService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)
        self.event_user_repository = EventUserRepository(db)
        self.content_repository = ContentRepository(db)
        self.user_repository = UserRepository(db)
        self.email_service = EmailService()


    def get_event_route(self, event_id: int):
        event = self.event_repository.search_event_by_id(event_id)
        if event:
            return event.route
        return None
    
    
    def get_event_subscribers(self, event_id: int) -> Optional[List]:
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

        contents = self.content_repository.get_contents_by_event(event_id=event_id)
        for c in contents:
            if c.language == user.language:
                return c.content
            if c.language == "EN":
                default_content = c
        return default_content.content
    
    
    def get_event_notification_data(self, event_id: int ) -> Optional[Dict]:
        route = self.get_event_route(event_id)
        if not route:
            return None
        
        subscribers = self.get_event_subscribers(event_id)
        notification_data = {
            "route": route,
            "subscribers": []
        }
        
        for subscriber in subscribers:
            content = self.get_event_content(event_id=event_id, user_id=subscriber)
            notification_data["subscribers"].append({
                "user_id": subscriber,
                "content": content
            })
        
        return notification_data
    
    
    def prepare_email_data(self, event_id: int) -> List[Dict]:
        event = self.event_repository.search_event_by_id(event_id)
        if not event:
            return None
        
        notification_data = self.get_event_notification_data(event_id)
        if not notification_data:
            return None
        
        subscribed_user_ids = [subscriber["user_id"] for subscriber in notification_data["subscribers"]]
        users = self.user_repository.get_users_by_user_ids(subscribed_user_ids)
        user_map = {}
        for user in users:
            user_map[user.id] = user
        
        email_data = []
        
        for subscriber in notification_data["subscribers"]:
            user = user_map.get(subscriber["user_id"])
            email_data.append({
                "To": user.username,
                "Subject": f"Notification for Event {event.name}",
                "body": subscriber["content"]
            })
        
        return email_data
    
    
    def send_email_notification(self, event_id: int):
        route = self.get_event_route(event_id)
        if route != "EMAIL":
            return None
        
        email_data = self.prepare_email_data(event_id)
        
        return self.email_service.send_emails(email_data_list=email_data)
    
    
    def process_event(self, event_id: int):
        route = self.get_event_route(event_id)
        if not route:
            return None
        
        if route == "EMAIL":
            success = self.send_email_notification(event_id)
            return "Emails sent" if success else "Failed sending emails"
        
        return None