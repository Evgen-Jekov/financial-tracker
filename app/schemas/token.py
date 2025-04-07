from pydantic import BaseModel, Field

class Token(BaseModel):
    user_id : int = Field(gt=0)
    access_token : str
    token_type : str