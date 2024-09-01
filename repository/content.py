from sqlalchemy.orm import Session

from database.event import Event
from database.user import User
from database.content import Content
from schema.database.content import ContentCreate


class ContentRepository:
    def __init__(self, db:Session):
        self.db = db
        
    
    def get_contents_by_event(self, event_id:int):
        return self.db.query(Content).filter(Content.event_id == event_id).all()
    
    
    def create_content(self, content:ContentCreate):
        db_content = Content(content=content.content,
                             event_id=content.event_id,
                             language=content.language)
        self.db.add(db_content)
        self.db.commit()
        self.db.refresh(db_content)
        return db_content
    
    
    # def update_content(self, content_id:int, content:Content):
    #     db_content = self.get_content(content.id)
    #     if db_content:
    #         db_content.content = content.content
    #         db_content.event_id = content.event_id
    #         db_content.language = content.language
    #         self.db.commit()
    #         self.db.refresh(db_content)
    #         return db_content
    #     return None
    
    
    # def delete_content(self, content:Content):
    #     self.db.delete(content)
    #     self.db.commit()
    #     return

