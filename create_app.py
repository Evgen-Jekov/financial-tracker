from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.connect import connect

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_methods='*',
        allow_headers='*',
        allow_credentials=True)

    connect(app=app)

    return app