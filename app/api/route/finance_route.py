from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user import get_current_user, oauth2_scheme
from app.schemas.schemas_finance import FinanceCreate, FinanceResponse
from app.model.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from app.model.model import Finance

route_finance = APIRouter(prefix='/finance', tags=['FINANCE'])


@route_finance.post('/add-finance', response_model=FinanceResponse)
def add_finance(finance : FinanceCreate,
                db : Annotated[Session, Depends(get_db)],
                token : Annotated[str, Depends(oauth2_scheme)]):
    try:
        data_user = get_current_user(token=token, db=db)

        if data_user.id != finance.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to view this user')
        
        new_finance = Finance()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))