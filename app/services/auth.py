from app.schemas import UserSchema, Token
from app.core.security import encode_jwt


class AuthService:
    def login(self, user: UserSchema) -> Token:
        return Token(
            access_token=encode_jwt(
                {
                    "sub": f"{user.id}",
                }
            ),
            token_type="Bearer"
        )
