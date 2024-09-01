from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.content import ContentRepository
from schema.database.content import ContentCreate

class ContentService:
    def __init__(self, db:Session):
        self.content_repository = ContentRepository(db)
        self.event_repository = EventRepository(db)
    
    
    def list_contents_by_event(self, event_id:int):
        return self.content_repository.get_contents_by_event(event_id)
    
    
    def create_content(self, user: dict, content: ContentCreate):
        if self.event_repository.search_event_by_id(content.event_id):
            new_content = self.content_repository.create_content(content=content)
            return new_content
        return None