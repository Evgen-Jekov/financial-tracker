from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm
from app.model.database import get_db
from app.model.model import User
from app.services.user import authenticate_user, create_user, oauth2_scheme, get_current_user, get_user
from app.schemas.schemas_user import UserCreate, UserResponses
from sqlalchemy.orm import Session
from typing import Annotated

route_user = APIRouter(prefix='/user', tags=['USER'])


@route_user.post(path='/login', response_model=UserResponses)
def login_user(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], 
               db : Annotated[Session, Depends(get_db)]):
    email = db.query(User).filter(User.username == form_data.username).first()

    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    data_user = UserCreate(
        username=form_data.username,
        email=email.email,
        password=form_data.password
        )

    token = authenticate_user(data_user=data_user, db=db)

    user = UserResponses(
        token=token['token'].access_token,
        create_at=token["user"].create_at,
        username=token["user"].username,
        email=token["user"].email
    )

    return user

@route_user.post('/register', response_model=UserResponses)
def register_user(data_user : UserCreate, 
                  db : Annotated[Session, Depends(get_db)]):
    check = db.query(User).filter(User.email == data_user.email).first()

    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user already exist')

    user = create_user(data_user=data_user, db=db)
    print(user)

    result_user = UserResponses(
        token=user["token"],
        create_at=user["user"].create_at,
        username=user["user"].username,
        email=user["user"].email
    )

    return result_user


def get_user_data(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Annotated[Session, Depends(get_db)], 
    id: Annotated[int, Path(gt=0)]
):
    current_user = get_current_user(token=token, db=db)

    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view this user")

    user = get_user(id=id, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    result_user = UserResponses(
        token=token,
        create_at=user.create_at,
        email=user.email,
        username=user.username
    )

    return result_user