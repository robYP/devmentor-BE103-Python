from sqlalchemy import Column, Integer, String

from infrastructure.mysql import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    langauge = Column(String(50))
