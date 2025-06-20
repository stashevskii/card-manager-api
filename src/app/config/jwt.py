from src.app.core.base import EnvConfig


class JWTConfig(EnvConfig):
    secret_key: str
    algorithm: str = "HS256"
