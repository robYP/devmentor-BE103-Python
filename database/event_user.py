from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base


class EventUser(Base):
    __tablename__ = 'event_user'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    notifiy_time = Column(DateTime, nullable=True)
    
    event = relationship('Event', 
                         primaryjoin='foreign(EventUser.event_id) == remote(Event.id)',
                         foreign_keys=[event_id],
                         back_populates='event_users')
    user = relationship('User', 
                        primaryjoin='foreign(EventUser.user_id) == remote(User.id)',
                        back_populates='event_users')