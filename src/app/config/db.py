from src.app.core.base import EnvConfig


class DbConfig(EnvConfig):
    postgres_user: str
    postgres_db: str
    postgres_password: str
