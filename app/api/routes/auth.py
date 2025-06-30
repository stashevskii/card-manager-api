from fastapi import APIRouter, Depends
from app.dependencies import AuthServiceDep, CurrentUserDep, verify_credentials
from app.models import User
from app.schemas import Token, UserSchema

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", summary="Get JWT token for auth")
def login(service: AuthServiceDep, user: User = Depends(verify_credentials)) -> Token:
    return service.login(user)


@router.get("/me", summary="Get current authed user")
def get_current_user(user: CurrentUserDep) -> UserSchema:
    return user
