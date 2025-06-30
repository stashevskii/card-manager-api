import datetime
import jwt
from app.config import config


def encode_jwt(payload: dict) -> str:
    now = datetime.datetime.now(datetime.UTC)
    payload["iat"] = now
    payload["exp"] = now + datetime.timedelta(minutes=30)
    return jwt.encode(payload, config.jwt_config.secret_key, algorithm=config.jwt_config.algorithm)


def decode_jwt(token: bytes | str) -> dict:
    return jwt.decode(token, config.jwt_config.secret_key, algorithms=[config.jwt_config.algorithm])
