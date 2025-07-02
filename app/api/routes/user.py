from fastapi import APIRouter, Depends
from app.utils import handle_business_errors
from app.schemas import (
    UserFilter,
    UserSchema,
    UserCreate,
    SuccessSchema,
    UserReplace,
    UserPU,
)
from app.dependencies import UserServiceDep, AdminDep

router = APIRouter(prefix="/api/admin/users", tags=["Users (Admin)"])


@router.get("/", summary="Get user by query")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, schema: UserFilter = Depends()) -> UserSchema:
    return service.get(schema)


@router.post("/", summary="Add user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, schema: UserCreate = Depends()) -> UserSchema:
    return service.add(schema)


@router.get("/all", summary="Get all users")
def get_users(_: AdminDep, service: UserServiceDep) -> list[UserSchema]:
    return service.get_all()


@router.get("/{id}", summary="Get user by id")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, id: int) -> UserSchema:
    return service.get_by_id(id)


@router.delete("/{id}", summary="Delete user")
@handle_business_errors
def delete_user(_: AdminDep, service: UserServiceDep, id: int) -> SuccessSchema:
    return service.delete(id)


@router.put("/{id}", summary="Replace user")
@handle_business_errors
def replace_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserReplace = Depends()) -> UserSchema:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Part update user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserPU = Depends()) -> UserSchema:
    return service.part_update(id, schema)
