from fastapi import APIRouter
from src.app.dependencies import AuthServiceDep, CurrentUserDep
from src.app.dependencies import VerifyCredentialsDep
from src.app.schemas import Token, UserSchema

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", summary="Get JWT token for auth")
def login(service: AuthServiceDep, user: VerifyCredentialsDep) -> Token:
    return service.login(user)


@router.get("/users/me", summary="Get current authed user")
def get_current_user(user: CurrentUserDep) -> UserSchema:
    return user
