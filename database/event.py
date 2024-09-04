from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base
from database.user import User
from database.event_user import EventUser


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    route = Column(String(255), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    creator_id = Column(Integer, nullable=False)

    creator = relationship('User', 
                           primaryjoin='foreign(Event.creator_id) == remote(User.id)',
                           back_populates='created_events')
    event_users = relationship('EventUser', 
                               primaryjoin='Event.id == foreign(remote(EventUser.event_id))',
                               back_populates='event')
    records = relationship('Record',
                           primaryjoin='Event.id == foreign(remote(Record.event_id))',
                           back_populates='event',
                           viewonly=True)
    contents = relationship('Content',
                            primaryjoin='Event.id == foreign(remote(Content.event_id))',
                            back_populates='event')