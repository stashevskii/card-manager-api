from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.app.api.errors import InvalidToken, ForbiddenResource, InvalidCredentials
from src.app.models import User, Card
from src.app.core.security import decode_jwt
from src.app.utils import UserRole, verify_password
from src.app.repositories import CardRepository, UserRepository
from src.app.schemas import Credentials
from src.app.services import AuthService, CardService, UserService
from src.app.core.db import get_db

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


def verify_credentials(schema: Credentials = Depends(), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter_by(username=schema.username).first()
    if user is None or not verify_password(schema.password, user.password, True):
        raise InvalidCredentials
    return user


def get_current_user(db: DbDep, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
    try:
        token = credentials.credentials
        user = db.query(User).filter_by(id=int(decode_jwt(token)["sub"])).first()
        return user
    except InvalidTokenError:
        raise InvalidToken


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def is_admin(current_user: CurrentUserDep) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenResource
    return current_user


AdminDep = Annotated[User, Depends(is_admin)]
