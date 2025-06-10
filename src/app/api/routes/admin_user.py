from fastapi import APIRouter, Depends
from src.app.utils import handle_business_errors
from src.app.schemas import (
    UserFilter,
    UserSchema,
    UserCreate,
    SuccessSchema,
    UserReplace,
    UserPU,
)
from src.app.dependencies import UserServiceDep, AdminDep

router = APIRouter(prefix="/api/admin/users", tags=["Users (Admin)"])


@router.get("/", summary="Get user by query")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, schema: UserFilter = Depends()) -> UserSchema:
    return service.admin_get(schema)


@router.post("/", summary="Add user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, schema: UserCreate = Depends()) -> UserSchema:
    return service.admin_add(schema)


@router.get("/all", summary="Get all users")
def get_users(_: AdminDep, service: UserServiceDep) -> list[UserSchema]:
    return service.admin_get_all()


@router.get("/{id}", summary="Get user by id")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, id: int) -> UserSchema:
    return service.admin_get_by_id(id)


@router.delete("/{id}", summary="Delete user")
@handle_business_errors
def delete_user(_: AdminDep, service: UserServiceDep, id: int) -> SuccessSchema:
    return service.admin_delete(id)


@router.put("/{id}", summary="Replace user")
@handle_business_errors
def replace_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserReplace = Depends()) -> UserSchema:
    return service.admin_replace(id, schema)


@router.patch("/{id}", summary="Part update user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserPU = Depends()) -> UserSchema:
    return service.admin_part_update(id, schema)
