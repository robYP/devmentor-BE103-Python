from sqlalchemy.orm import Session
from repository.event import EventRepository
from repository.content import ContentRepository
from repository.record import RecordRepository
from schema.database.content import ContentCreate
from schema.database.language import Language

class ContentService:
    def __init__(self, db:Session):
        self.content_repository = ContentRepository(db)
        self.event_repository = EventRepository(db)
        self.record_repository = RecordRepository(db)
    
    
    def list_contents_by_event(self, event_id:int):
        return self.content_repository.get_contents_by_event(event_id)
    
    
    def create_content(self, user: dict, content: ContentCreate, event_id: int, language: Language):
        event_exists = self.event_repository.search_event_by_id(event_id)
        content_exists = self.content_repository.get_content(event_id=event_id, language=language)
    
        if event_exists and not content_exists:
            new_content = self.content_repository.create_content(content=content, event_id=event_id, language=language)
            self.record_repository.create_record(user_id = user.id,
                                       event_id = event_id,
                                       action = "Create Content")
            return new_content
        
        return None
    
    
    def update_content(self, user:dict, content: ContentCreate, event_id: int, language: Language):
        event_exists = self.event_repository.search_event_by_id(event_id)
        content_exists = self.content_repository.get_content(event_id=event_id, language=language)
        
        if event_exists and content_exists:
            updated_content = self.content_repository.update_content(content_exisits=content_exists, updated_content=content)
            self.record_repository.create_record(user_id = user.id,
                                       event_id = updated_content.event_id,
                                       action = "Update Content")
            return updated_content
        return None
    
    
    def delete_content(self, user:dict, event_id:int, language:str):
        event_exists = self.event_repository.search_event_by_id(event_id=event_id)
        content_exists = self.content_repository.get_content(event_id=event_id, language=language)
        
        if event_exists and content_exists: 
            deleted_content = self.content_repository.delete_content(content_exists)
            self.record_repository.create_record(user_id = user.id,
                                       event_id = content_exists.event_id,
                                       action = "Delete Content")
            return deleted_content
        return None