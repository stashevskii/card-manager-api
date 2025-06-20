from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from src.app.api.errors import register_errors_handler
from src.app.core.base import Base
from src.app.config import config
from src.app.core.db import engine, get_db
from src.app.api.routes import register_main_router
from src.app.enums import UserRole
from src.app.models import User
from src.app.utils import hash_password


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    admin = User(
        username="admin",
        email="admin@admin.com",
        password=hash_password("qwerty"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()

    yield


def create_app() -> FastAPI:
    application = FastAPI(
        debug=config.app_config.app_debug,
        title=config.app_config.app_title,
        version=config.app_config.app_version,
        description=config.app_config.app_description,
        lifespan=lifespan
    )
    register_main_router(application)
    register_errors_handler(application)
    return application


def run():
    uvicorn.run(
        app="src.app.main:app",
        host=config.app_config.app_host,
        port=config.app_config.app_port,
        reload=True
    )


app = create_app()
