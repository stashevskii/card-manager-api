from fastapi import APIRouter, Depends
from src.app.core.utils import handle_business_errors
from src.app.schemas import (
    UserFilter,
    UserSchema,
    UserCreate,
    SuccessSchema,
    UserReplace,
    UserPU,
    CardPU,
    CardSchema,
    OwnerCardSchema,
    CardReplace,
    CardCreate, CardBlockResponse,
)
from src.app.dependencies import UserServiceDep, CardServiceDep, AdminDep

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users", summary="Get user by query")
@handle_business_errors
def get_user(_: AdminDep, service: UserServiceDep, schema: UserFilter = Depends()) -> UserSchema:
    return service.admin_get(schema)


@router.get("/users/all", summary="Get all users")
def get_users(_: AdminDep, service: UserServiceDep) -> list[UserSchema]:
    return service.admin_get_all()


@router.get("/cards/all", summary="Get all cards")
def get_all_cards(_: AdminDep, service: CardServiceDep) -> list[OwnerCardSchema]:
    return service.admin_get_all()


@router.post("/users", summary="Add user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, schema: UserCreate = Depends()) -> UserSchema:
    return service.admin_add(schema)


@router.post("/cards", summary="Add card")
@handle_business_errors
def add_card(_: AdminDep, service: CardServiceDep, schema: CardCreate = Depends()) -> CardSchema:
    return service.admin_add(schema)


@router.delete("/users/{id}", summary="Delete user")
@handle_business_errors
def delete_user(_: AdminDep, service: UserServiceDep, id: int) -> SuccessSchema:
    return service.admin_delete(id)


@router.delete("/cards/{id}", summary="Delete card")
@handle_business_errors
def delete_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_delete(id)


@router.put("/users/{id}", summary="Replace user")
@handle_business_errors
def replace_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserReplace = Depends()) -> UserSchema:
    return service.admin_replace(id, schema)


@router.put("/cards/{id}", summary="Replace card")
@handle_business_errors
def replace_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardReplace = Depends()) -> CardSchema:
    return service.admin_replace(id, schema)


@router.patch("/users/{id}", summary="Part update user")
@handle_business_errors
def add_user(_: AdminDep, service: UserServiceDep, id: int, schema: UserPU = Depends()) -> UserSchema:
    return service.admin_part_update(id, schema)


@router.patch("/cards/{id}", summary="Part update card")
@handle_business_errors
def part_update_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardPU = Depends()) -> CardSchema:
    return service.admin_part_update(id, schema)


@router.patch("/cards/block/{id}", summary="Block card")
@handle_business_errors
def block_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_block(id)


@router.get("/cards/get-required-blocks", summary="Get all required card blocks from users")
@handle_business_errors
def get_required_card_blocks(_: AdminDep, service: CardServiceDep) -> list[CardBlockResponse]:
    return service.admin_get_required_blocks()


@router.patch("/cards/activate/{id}", summary="Activate (reblock) card")
@handle_business_errors
def activate_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_activate(id)
