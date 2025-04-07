import jwt
from jwt.exceptions import InvalidTokenError
import os
from fastapi import Depends, HTTPException, status
from app.model.database import get_db
from app.model.model import User
from app.schemas.schemas_user import UserCreate
from app.schemas.token import Token
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone

load_dotenv()

SECRET_KEY = os.getenv('JWT')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=15)
pwd_context = CryptContext(['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data : dict, expires_delta : Annotated[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def authenticate_user(data_user : UserCreate, db : Annotated[Session, Depends(get_db)]) -> Token:
    check = db.query(User).filter(User.username == data_user.username).first()

    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    if not verify_password(data_user.password, check.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='innocorect username or password')
    
    token_access = create_access_token(data={"sub" : data_user.username}, 
                                       expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(access_token=token_access, token_type="bearer", user_id=check.id)

def create_user(data_user : UserCreate, db : Annotated[Session, Depends(get_db)]):
    try:
        password = get_password_hash(data_user.password)

        new_user = User(username=data_user.username, 
                        password=password, 
                        email=data_user.email)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token(data={"sub" : data_user.username}, 
                                       expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

        return {'user' : new_user, 'token' : token}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def get_user(username: str, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not auth')

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        return user

    except InvalidTokenError as e:
        raise error

        