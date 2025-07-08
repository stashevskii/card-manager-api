from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import User, Card
from app.core.security import decode_jwt
from app.core.enums import UserRole
from app.utils import verify_password
from app.repositories import CardRepository, UserRepository
from app.schemas import Credentials
from app.services import AuthService, CardService, UserService
from app.core.db import get_db

DbDep = Annotated[Session, Depends(get_db)]


def get_user_repository(db: DbDep) -> UserRepository:
    return UserRepository(db, User)


def get_card_repository(db: DbDep) -> CardRepository:
    return CardRepository(db, Card)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


def get_card_service(card_repository: CardRepository = Depends(get_card_repository)) -> CardService:
    return CardService(card_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

CardServiceDep = Annotated[CardService, Depends(get_card_service)]

AuthServiceDep = Annotated[AuthService, Depends(AuthService)]


def verify_credentials(schema: Credentials, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter_by(username=schema.username).first()
    if user is None or not verify_password(schema.password, user.password, True):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return user


def get_current_user(db: DbDep, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
    try:
        token = credentials.credentials
        user = db.query(User).filter_by(id=int(decode_jwt(token)["sub"])).first()
        return user
    except InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def is_admin(current_user: CurrentUserDep) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
    return current_user


AdminDep = Annotated[User, Depends(is_admin)]
