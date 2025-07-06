from fastapi import APIRouter, Depends
from app.utils import handle_business_errors
from app.schemas import (
    UserFilter,
    UserSchema,
    UserCreate,
    UserReplace,
    UserPU,
)
from app.dependencies import UserServiceDep, AdminDep

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", summary="Get list of users by query. For admin only")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, schema: UserFilter = Depends()) -> list[UserSchema]:
    return service.get(schema)


@router.post("/", status_code=201, summary="Create user. For admin only")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, schema: UserCreate) -> UserSchema:
    return service.add(schema)


@router.get("/{id}", summary="Get user by id. For admin only")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, id: int) -> UserSchema:
    return service.get_by_id(id)


@router.delete("/{id}", status_code=204, summary="Delete user. For admin only")
@handle_business_errors
def delete_user(_: AdminDep, service: UserServiceDep, id: int):
    return service.delete(id)


@router.put("/{id}", summary="Replace user. For admin only")
@handle_business_errors
def replace_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserReplace) -> UserSchema:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Update user. For admin only")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserPU) -> UserSchema:
    return service.part_update(id, schema)
