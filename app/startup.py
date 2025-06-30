from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.api.errors import register_errors_handler
from app.core.base import Base
from app.config import config
from app.core.db import engine, get_db
from app.api.routes import register_main_router
from app.enums import UserRole
from app.models import User
from app.utils import hash_password


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = next(get_db())
    if not db.query(User).filter_by(username="admin", email="admin@admin.com").first():
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
        app="app.main:app",
        host=config.app_config.app_host,
        port=config.app_config.app_port,
        reload=True
    )


app = create_app()
