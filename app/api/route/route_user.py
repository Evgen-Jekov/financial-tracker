from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.model.database import get_db
from app.model.user import User
from app.services.user import authenticate_user
from app.schemas.schemas_user import UserCreate, UserResponses
from sqlalchemy.orm import Session

route_user = APIRouter(prefix='/user', tags=['USER'])


route_user.post(path='/login', response_model=UserResponses)
def login_user(form_data : OAuth2PasswordRequestForm, db : Session = Depends(get_db)):
    email = db.query(User).filter(User.username == form_data.username).first()


    data_user = UserCreate(
        username=form_data.username,
        email=email.email,
        password=form_data.password
        )

    token = authenticate_user(data_user=data_user, db=db)

    return {'user' : data_user, 'token' : token}