from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
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
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    creator = relationship('User', back_populates='created_events')
    event_users = relationship('EventUser', back_populates='event')
