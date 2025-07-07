from app.schemas import UserSchema, Token
from app.core.security import encode_jwt


class AuthService:
    @staticmethod
    def login(user: UserSchema) -> Token:
        return {"access_token": encode_jwt({"sub": f"{user.id}"}), "token_type": "Bearer"}
