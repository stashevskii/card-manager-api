from fastapi import FastAPI
from .process_time import ProcessTimeMiddleware


def register_middlewares(app: FastAPI):
    app.add_middleware(ProcessTimeMiddleware)
