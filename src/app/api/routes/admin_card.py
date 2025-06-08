from fastapi import APIRouter, Depends
from src.app.core.utils import handle_business_errors
from src.app.schemas import (
    SuccessSchema,
    CardPU,
    CardSchema,
    OwnerCardSchema,
    CardReplace,
    CardCreate, CardBlockResponse, CardFilter,
)
from src.app.dependencies import CardServiceDep, AdminDep

router = APIRouter(prefix="/api/admin/cards", tags=["Cards (Admin)"])


@router.get("/", summary="Get card by query")
@handle_business_errors
def get_all_cards(_: AdminDep, service: CardServiceDep, schema: CardFilter = Depends()) -> list[OwnerCardSchema]:
    return service.admin_get(schema)


@router.get("/all", summary="Get all cards")
def get_all_cards(_: AdminDep, service: CardServiceDep) -> list[OwnerCardSchema]:
    return service.admin_get_all()


@router.post("/", summary="Add card")
@handle_business_errors
def add_card(_: AdminDep, service: CardServiceDep, schema: CardCreate = Depends()) -> CardSchema:
    return service.admin_add(schema)


@router.get("/{id}", summary="Get card by id")
@handle_business_errors
def get_all_cards(_: AdminDep, service: CardServiceDep, id: int) -> list[OwnerCardSchema]:
    return service.admin_get_by_id(id)


@router.delete("/{id}", summary="Delete card")
@handle_business_errors
def delete_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_delete(id)


@router.put("/{id}", summary="Replace card")
@handle_business_errors
def replace_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardReplace = Depends()) -> CardSchema:
    return service.admin_replace(id, schema)


@router.patch("/{id}", summary="Part update card")
@handle_business_errors
def part_update_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardPU = Depends()) -> CardSchema:
    return service.admin_part_update(id, schema)


@router.patch("/{id}/block", summary="Block card")
@handle_business_errors
def block_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_block(id)


@router.patch("/{id}/activate", summary="Activate (reblock) card")
@handle_business_errors
def activate_card(_: AdminDep, service: CardServiceDep, id: int) -> SuccessSchema:
    return service.admin_activate(id)


@router.get("/pending-blocks", summary="Get all required card blocks from users")
@handle_business_errors
def get_required_card_blocks(_: AdminDep, service: CardServiceDep) -> list[CardBlockResponse]:
    return service.admin_get_required_blocks()
