from app.core.base import BaseSchema


class Credentials(BaseSchema):
    username: str
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str
