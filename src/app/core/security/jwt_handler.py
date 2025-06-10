import datetime
import jwt
from src.app.config import config


def encode_jwt(
        payload: dict,
        key: str = config.jwt_config.private_key,
        algorithm: str = config.jwt_config.algorithm,
) -> str:
    now = datetime.datetime.now(datetime.UTC)
    payload["iat"] = now
    payload["exp"] = now + datetime.timedelta(minutes=30)
    return jwt.encode(payload, key, algorithm=algorithm)


def decode_jwt(
        token: bytes | str,
        key: str = config.jwt_config.public_key,
        algorithm: str = config.jwt_config.algorithm
) -> dict:
    return jwt.decode(token, key, algorithms=[algorithm])
