from app.api.route import route_user
from app.api.route import route_finance
from fastapi import FastAPI


def connect(app : FastAPI):
    app.include_router(route_user.route_user)
    app.include_router(route_finance.route_finance)