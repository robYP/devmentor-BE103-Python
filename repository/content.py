from sqlalchemy.orm import Session

from database.content import Content
from schema.database.content import ContentCreate
from schema.database.language import Language


class ContentRepository:
    def __init__(self, db:Session):
        self.db = db
        
    
    def get_contents_by_event(self, event_id:int):
        return self.db.query(Content).filter(Content.event_id == event_id).all()
    
    
    def get_content(self, event_id:int, language:str):
        return self.db.query(Content).filter(Content.event_id == event_id, 
                                             Content.language == language).first()
    
    
    def create_content(self, content:ContentCreate, event_id:int, language: Language):
        db_content = Content(content=content.content,
                             event_id=event_id,
                             language=language)
        self.db.add(db_content)
        self.db.commit()
        self.db.refresh(db_content)
        return db_content
    
    
    def update_content(self, content_exisits: Content, updated_content:Content):
        content_exisits.content = updated_content.content
        self.db.commit()
        self.db.refresh(content_exisits)
        return content_exisits
    
    
    def delete_content(self,content:Content):
        self.db.delete(content)
        self.db.commit()
        return content

