from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from app.services.user import get_current_user, oauth2_scheme
from app.schemas.schemas_finance import FinanceCreate, FinanceResponse, FinanceList, FinanceDelete
from app.model.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app.services.finance import create_finance, get_all, get_category, delete_finance

route_finance = APIRouter(prefix='/finance', tags=['FINANCE'])


@route_finance.post('/add-finance', response_model=FinanceResponse)
def add_finance(finance : FinanceCreate,
                db : Annotated[Session, Depends(get_db)],
                token : Annotated[str, Depends(oauth2_scheme)]):
    data_user = get_current_user(token=token, db=db)

    if data_user.id != finance.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to view this user')
        
    response = create_finance(data_finance=finance, db=db)

    return response


@route_finance.get('/get-all-finance', response_model=FinanceList)
def get_all_finance(db : Annotated[Session, Depends(get_db)],
                token : Annotated[str, Depends(oauth2_scheme)]):
    
    user = get_current_user(token=token, db=db)
    all_finance = get_all(data_user=user, db=db)
    list_fin = []

    for fin in all_finance: 
        list_fin.append(FinanceResponse(
            success=True,
            user_id=fin.user_id,
            category=fin.category,
            name_of_the_expenditure=fin.name_of_the_expenditure,
            amount=fin.amount,
            create_at=fin.create_at
        ))

    return FinanceList(finance=list_fin)

@route_finance.post('/get-category-finance', response_model=FinanceList)
def get_category(db : Annotated[Session, Depends(get_db)],
                token : Annotated[str, Depends(oauth2_scheme)],
                category : Annotated[str, Body()]):
    user = get_current_user(token=token, db=db)
    category_all = get_category(category=category, data_user=user, db=db)
    list_category = []

    for cat in category_all:
        list_category.append(FinanceResponse(
            user_id=cat.user_id,
            category=cat.category,
            name_of_the_expenditure=cat.name_of_the_expenditure,
            amount=cat.amount,
            success=True,
            create_at=cat.create_at
        ))

    return FinanceList(finance=list_category)

@route_finance.delete('/delete-finance/{id}', response_model=FinanceDelete)
def del_finance(db : Annotated[Session, Depends(get_db)],
                token : Annotated[str, Depends(oauth2_scheme)],
                id : Annotated[int, Path]):
    user = get_current_user(token=token, db=db)
    responses = delete_finance(data_user=user, id=id, db=db)

    if responses:
        return FinanceDelete(status='Success delete')
    else:
        return FinanceDelete(status='Unsuccess delete')