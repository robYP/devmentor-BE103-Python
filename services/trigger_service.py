from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.event_user import EventUserRepository
from repository.content import ContentRepository
from repository.user import UserRepository
from typing import Optional, List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import GMAIL_SMTP_SERVER, GMAIL_TLS_PORT, GMAIL_SMTP_USERNAME, GMAIL_SMTP_PASSWORD


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

        content = self.content_repository.get_content(event_id=event_id, language=user.language)
        return content.content if content else None
    
    
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
    
    
    def send_email_notification(self, event_id: int):
        event = self.event_repository.search_event_by_id(event_id)
        if not event:
            return None
        
        route = self.get_event_route(event_id)
        if route != "EMAIL":
            return None
        
        notification_data = self.get_event_notification_data(event_id)
        if not notification_data:
            return None
        
        with smtplib.SMTP(GMAIL_SMTP_SERVER) as connection:
            connection.starttls()
            connection.login(user=GMAIL_SMTP_USERNAME, password=GMAIL_SMTP_PASSWORD)
            
            for subscriber in notification_data["subscribers"]:
                user = self.user_repository.get_user_by_user_id(subscriber["user_id"])
                if not user:
                    continue
                
                msg = MIMEMultipart()
                msg["From"] = GMAIL_SMTP_USERNAME
                msg["To"] = user.username
                msg["Subject"] = f"Notification for Event {event.name}, {event_id}"
                
                body = subscriber["content"]
                msg.attach(MIMEText(body, "plain"))
                
                connection.send_message(msg)
                print(f"Email sent to {user.username}")
            
        return
    
    
    def process_event(self, event_id: int):
        route = self.get_event_route(event_id)
        if not route:
            return None
        
        if route == "EMAIL":
            self.send_email_notification(event_id)
            return "email sent"
        
        return None