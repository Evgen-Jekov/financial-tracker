from fastapi import APIRouter, Depends, HTTPException, status
from app.model.database import get_db
from app.model.user import User
from app.services.user import authenticate_user
from app.schemas.schemas_user import UserCreate, UserResponses
from sqlalchemy.orm import Session

route_user = APIRouter(prefix='/user', tags=['USER'])


route_user.post(path='/login', response_model=UserResponses)
def login_user(data_user : UserCreate, db : Session = Depends(get_db)):
    token = authenticate_user(data_user=data_user, db=db)

    return {'user' : data_user, 'token' : token}