from pathlib import Path
from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    public_key: str = (Path(__file__).parent.parent / "core" / "security" / "certs" / "public.pem").read_text()
    private_key: str = (Path(__file__).parent.parent / "core" / "security" / "certs" / "private.pem").read_text()
    algorithm: str = "RS256"
