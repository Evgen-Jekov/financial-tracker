from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        allow_origins='*',
        allow_methods='*',
        allow_headers='*',
        allow_credentials=True)

    return app