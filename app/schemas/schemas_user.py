from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
import re

class UserBase(BaseModel):
    username : str = Field(min_length=3, max_length=50)
    email : EmailStr = Field(min_length=8, max_length=128)


class UserResponses(UserBase):
    pass


class UserCreate(UserBase):
    password : str = Field(min_length=8, max_length=128)
    create_at : datetime

    @field_validator('password')
    def validate_password(cls, value):
        response = bool(re.fullmatch(pattern=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$'), value)

        if response == False:
            raise ValueError('Invalid password or username')
        
        return value