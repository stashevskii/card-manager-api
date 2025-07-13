from fastapi import APIRouter, Depends, status
from app.utils import handle_business_errors
from app.schemas import (
    UserFilter,
    UserSchema,
    UserCreate,
    UserReplace,
    UserUpdate,
)
from app.dependencies import UserServiceDep, AdminDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", summary="Get list of users by query. For admin only")
@handle_business_errors
def get_users_by_query(_: AdminDep, service: UserServiceDep, schema: UserFilter = Depends()) -> list[UserSchema]:
    return service.get(schema)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create user. For admin only")
@handle_business_errors
def create_user(_: AdminDep, service: UserServiceDep, schema: UserCreate) -> UserSchema:
    return service.create(schema)


@router.get("/{id}", summary="Get user by id. For admin only")
@handle_business_errors
def get_user_by_id(_: AdminDep, service: UserServiceDep, id: int) -> UserSchema:
    return service.get_by_id(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user. For admin only")
@handle_business_errors
def delete_user(_: AdminDep, service: UserServiceDep, id: int):
    return service.delete(id)


@router.put("/{id}", summary="Replace user. For admin only")
@handle_business_errors
def replace_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserReplace) -> UserSchema:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Update user. For admin only")
@handle_business_errors
def update_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserUpdate) -> UserSchema:
    return service.update(id, schema)
