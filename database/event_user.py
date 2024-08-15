from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base


class EventUser(Base):
    __tablename__ = 'event_user'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    notifiy_time = Column(DateTime, nullable=False)
    
    event = relationship('Event', back_populates='event_users')
    user = relationship('User', back_populates='event_users')