from fastapi import APIRouter
from app.services.user import get_current_user


route_finance = APIRouter(prefix='finance')