from app.api.route import route_user
from fastapi import FastAPI


def connect(app : FastAPI):
    app.include_router(route_user.route_user)