from .database import base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship

class Finance(base):    
    __tablename__ = 'finances'

    id = Column(Integer, primary_key=True, index=True)
    name_of_the_expenditure = Column(String(128), nullable=False)
    amount = Column(Integer, nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='spending')