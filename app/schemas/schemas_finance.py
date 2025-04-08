from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class FinanceCreate(BaseModel):
    user_id : int = Field(gt=0)
    category : Literal['Food', 'Transport', 'Housing',
                       'Health', 'Clothes and shoes', 'Entertainment and leisure',
                       'Education', 'Gifts and charity', 'Pets',
                       'Personal expenses', 'Trips', 'Savings and Investments', 
                       'Other']
    name_of_the_expenditure : str = Field(min_length=10, max_length=128)
    amount : int = Field(gt=0)

    class Config:
        from_attributes = True

class FinanceResponse(FinanceCreate):
    id : int
    success : bool = True
    user_id : int = Field(gt=0)
    name_of_the_expenditure : str = Field(min_length=10, max_length=128)
    category : Literal['Food', 'Transport', 'Housing',
                       'Health', 'Clothes and shoes', 'Entertainment and leisure',
                       'Education', 'Gifts and charity', 'Pets',
                       'Personal expenses', 'Trips', 'Savings and Investments', 
                       'Other']
    amount : int = Field(gt=0)
    create_at : datetime

    class Config:
        from_attributes = True

class FinanceList(BaseModel):
    finance : list[FinanceResponse]

class FinanceDelete(BaseModel):
    status : Literal['Success delete', 'Unsuccess delete']

class FinanceUpdateFull(BaseModel):
    category : Literal['Food', 'Transport', 'Housing',
                       'Health', 'Clothes and shoes', 'Entertainment and leisure',
                       'Education', 'Gifts and charity', 'Pets',
                       'Personal expenses', 'Trips', 'Savings and Investments', 
                       'Other']
    name_of_the_expenditure : str = Field(min_length=10, max_length=128)
    amount : int = Field(gt=0)