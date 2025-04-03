from pydantic import BaseModel, Field
from datetime import datetime

class FinanceCreate(BaseModel):
    user_id : int = Field(gt=0)
    name_of_the_expenditure : str = Field(min_length=10, max_length=128)
    amount : int = Field(gt=0)

    class Config:
        from_attributes = True

class FinanceResponse(FinanceCreate):
    create_at : datetime

    class Config:
        from_attributes = True