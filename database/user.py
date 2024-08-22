from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    language = Column(String(50), default="zh-TW")
    
    created_events = relationship('Event', back_populates='creator')
    event_users = relationship('EventUser', back_populates='user')
