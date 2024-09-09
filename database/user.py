from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.mysql import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=True)
    language = Column(String(50), default="ZH")
    line_user_id = Column(String(255), unique=True, nullable=True)
    
    created_events = relationship('Event', 
                                  primaryjoin='User.id == foreign(remote(Event.creator_id))',
                                  back_populates='creator')
    event_users = relationship('EventUser', 
                               back_populates='user',
                               primaryjoin='User.id == foreign(remote(EventUser.user_id))',
                               )
    records = relationship('Record', 
                           primaryjoin='User.id == foreign(remote(Record.user_id))',
                           back_populates='user')
