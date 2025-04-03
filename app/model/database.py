from sqlalchemy import create_engine, Column, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL =  os.getenv('DB')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sesion_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

def get_db():
    db = sesion_local()
    try:
        yield db
    finally:
        db.close()