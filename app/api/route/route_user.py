from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.model.database import get_db
from app.model.model import User
from app.services.user import authenticate_user, create_user
from app.schemas.schemas_user import UserCreate, UserResponses
from sqlalchemy.orm import Session

route_user = APIRouter(prefix='/user', tags=['USER'])


@route_user.post(path='/login', response_model=UserResponses)
def login_user(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    email = db.query(User).filter(User.username == form_data.username).first()

    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='data user not found')

    data_user = UserCreate(
        username=form_data.username,
        email=email.email,
        password=form_data.password
        )

    token = authenticate_user(data_user=data_user, db=db)

    return UserResponses(
        token=token['token'].access_token,
        create_at=token["user"].create_at,
        username=token["user"].username,
        email=token["user"].email
    )

@route_user.post('/register', response_model=UserResponses)
def register_user(data_user : UserCreate, db : Session = Depends(get_db)):
    check = db.query(User).filter(User.email == data_user.email).first()

    if check != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user already exist')

    user = create_user(data_user=data_user, db=db)

    return UserResponses(
        token=user["token"],
        create_at=user["user"].create_at,
        username=user["user"].username,
        email=user["user"].email
    )