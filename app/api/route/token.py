from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas.token import Token

route = APIRouter(tags=['TOKEN'])

route.post('/token')
async def token(from_data : Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    pass