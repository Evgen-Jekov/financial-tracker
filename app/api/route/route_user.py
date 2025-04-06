from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from fastapi.security import OAuth2PasswordRequestForm
from app.model.database import get_db
from app.model.model import User
from app.services.user import authenticate_user, create_user, oauth2_scheme, get_current_user, get_user
from app.schemas.schemas_user import UserCreate, UserResponses
from app.schemas.token import Token
from sqlalchemy.orm import Session
from typing import Annotated

route_user = APIRouter(prefix='/user', tags=['USER'])


@route_user.post(path='/login', response_model=Token)
def login_user(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], 
               db : Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    data_user = UserCreate(
        id=user.id,
        username=form_data.username,
        email=user.email,
        password=form_data.password
        )

    token = authenticate_user(data_user=data_user, db=db)


    return token['token']

@route_user.post('/register', response_model=UserResponses)
def register_user(data_user : UserCreate, 
                  db : Annotated[Session, Depends(get_db)]):
    check = db.query(User).filter(User.email == data_user.email).first()

    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user already exist')

    user = create_user(data_user=data_user, db=db)
    print(user)

    result_user = UserResponses(
        id=user['user'].id,
        token=user["token"],
        create_at=user["user"].create_at,
        username=user["user"].username,
        email=user["user"].email
    )

    return result_user

@route_user.post(path='/get-user/{id}', response_model=UserResponses)
def get_user_data(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Annotated[Session, Depends(get_db)], 
    id: Annotated[int, Path(gt=0)]
):
    current_user = get_current_user(token=token, db=db)

    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view this user")

    
    result_user = UserResponses(
        id=current_user.id,
        token=token,
        create_at=current_user.create_at,
        email=current_user.email,
        username=current_user.username
    )

    return result_user