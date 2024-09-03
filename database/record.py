from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base
from database.user import User
from database.event_user import EventUser


class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    action = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=True)
    event_id = Column(Integer, nullable=True)
    
    user = relationship("User", 
                        primaryjoin='foreign(Record.user_id) == remote(User.id)',
                        foreign_keys=[user_id],
                        back_populates="records")
    event = relationship("Event",
                         primaryjoin='foreign(Record.event_id) == remote(Event.id)',
                         foreign_keys=[event_id],
                         back_populates="records",
                         viewonly=True)