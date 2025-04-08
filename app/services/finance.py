from app.schemas.schemas_finance import FinanceCreate, FinanceResponse, FinanceUpdateFull
from fastapi import Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app.model.database import get_db
from app.model.model import Finance, User

def create_finance(data_finance : FinanceCreate, db : Annotated[Session, Depends(get_db)]):
    try:
        new_finance = Finance(category=data_finance.category, amount=data_finance.amount,
                            user_id=data_finance.user_id,
                            name_of_the_expenditure=data_finance.name_of_the_expenditure)
        
        db.add(new_finance)
        db.commit()
        db.refresh(new_finance)

        result = FinanceResponse(user_id=new_finance.user_id, category=new_finance.category,
                                name_of_the_expenditure=new_finance.name_of_the_expenditure,
                                amount=new_finance.amount, create_at=new_finance.create_at, 
                                success=True, id=new_finance.id)

        return result
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def delete_finance(data_user : User, id : int, db : Annotated[Session, Depends(get_db)]):
    try:
        del_finance = db.query(Finance).filter(Finance.user_id == data_user.id).filter(Finance.id == id).first()

        if not del_finance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='finance not found')

        db.delete(del_finance)
        db.commit()

        return True

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def update_full_finance(data_update : FinanceUpdateFull, 
                        data_user : User, id : int, 
                        db : Annotated[Session, Depends(get_db)]):
    try:
        update_full_finance = db.query(Finance).filter(
        Finance.user_id == data_user.id).filter(Finance.id == id).update(
            {Finance.category : data_update.category,
             Finance.amount : data_update.amount,
             Finance.name_of_the_expenditure : data_update.name_of_the_expenditure,
             Finance.create_at : func.now(),
             }, synchronize_session="fetch")
        
        if update_full_finance == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="finance not found")
        
        db.commit()

        updated_finance = db.query(Finance).filter(
            Finance.user_id == data_user.id).filter(Finance.id == id).first()
    
        return updated_finance
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def get_all(data_user : User, db : Annotated[Session, Depends(get_db)]):
    try:
        finance = db.query(Finance).filter(Finance.user_id == data_user.id).all()

        return finance
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def get_category(category : str, data_user : User, db : Annotated[Session, Depends(get_db)]):
    try:
        categ = db.query(Finance).filter(Finance.user_id == data_user.id).filter(Finance.category == category).all()

        if not categ:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='finance not found')

        return categ
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
