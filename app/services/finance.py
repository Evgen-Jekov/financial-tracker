from app.schemas.schemas_finance import FinanceCreate, FinanceResponse
from fastapi import Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
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
                                success=True)

        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()
    

def get_all(data_user : User, db : Annotated[Session, Depends(get_db)]):
    try:
        finance = db.query(Finance).filter(Finance.user_id == data_user.id).all()

        return finance
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()
    

def get_ctegory(category : str, data_user : User, db : Annotated[Session, Depends(get_db)]):
    try:
        categ = db.query(Finance).filter(Finance.user_id == data_user.id).filter(Finance.category == category).all()

        return categ
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()
