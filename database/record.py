from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base
from database.user import User
from database.event_user import EventUser


class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    action = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    
    user = relationship("User", back_populates="records")
    event = relationship("Event", back_populates="records")