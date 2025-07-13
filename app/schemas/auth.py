from app.core.base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str
