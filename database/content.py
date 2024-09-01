from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base

class Content(Base):
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    event_id = Column(Integer, nullable=False)
    language = Column(String(50), nullable=False)

    event = relationship('Event',
                         primaryjoin='foreign(Content.event_id) == remote(Event.id)',
                         foreign_keys=[event_id],
                         back_populates='contents')