from pydantic_settings import BaseSettings
from .app import AppConfig
from .db import DbConfig
from .jwt import JWTConfig


class Config(BaseSettings):
    db_config: DbConfig = DbConfig()
    app_config: AppConfig = AppConfig()
    jwt_config: JWTConfig = JWTConfig()


config = Config()
