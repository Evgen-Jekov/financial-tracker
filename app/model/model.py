from .database import base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    spending = relationship('Finance', back_populates='user')


class Finance(base):    
    __tablename__ = 'finances'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    name_of_the_expenditure = Column(String(128), nullable=False)
    amount = Column(Integer, nullable=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='spending')