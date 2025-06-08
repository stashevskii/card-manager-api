from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.app.api.errors import InvalidToken, ForbiddenResource, InvalidCredentials
from src.app.models import User, Card
from src.app.core.security import decode_jwt
from src.app.core.utils import UserRole, verify_passwords
from src.app.repositories import CardRepository, UserRepository
from src.app.schemas import Credentials
from src.app.services import AuthService, CardService, UserService
from src.app.core.db import get_db

DbDep = Annotated[Session, Depends(get_db)]


def get_user_repository(db: DbDep) -> UserRepository:
    return UserRepository(db, User)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_card_repository(db: DbDep) -> CardRepository:
    return CardRepository(db, Card)


CardRepositoryDep = Annotated[CardRepository, Depends(get_card_repository)]


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_card_service(card_repository: CardRepositoryDep, user_repository: UserRepositoryDep) -> CardService:
    return CardService(card_repository, user_repository)


CardServiceDep = Annotated[CardService, Depends(get_card_service)]

AuthServiceDep = Annotated[AuthService, Depends(AuthService)]


def verify_credentials(schema: Credentials = Depends(), db: Session = Depends(get_db)) -> type[User]:
    user = db.query(User).filter_by(username=schema.username).first()
    if user is None or not verify_passwords(schema.password, user.password, True):
        raise InvalidCredentials
    return user


VerifyCredentialsDep = Annotated[User, Depends(verify_credentials)]


def get_current_user(db: DbDep, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> type[User]:
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
