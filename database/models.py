from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text, Boolean, Float, Date, VARCHAR, column, ARRAY
from datetime import datetime

from .db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    max_id = Column(BigInteger, unique=True)
    username = Column(Text)
    full_name = Column(Text)
    campaign_id = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

class Default(Base):
    __tablename__ = "default"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    message = Column(String)
    links = Column(ARRAY(Text))
    count_transitions = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
