from typing import Annotated

from fastapi import APIRouter, Depends, Path
from app.enums import CardStatus
from app.utils import handle_business_errors
from app.schemas import (
    SuccessSchema,
    CardPU,
    CardSchema,
    OwnerCardSchema,
    CardReplace,
    CardCreate, CardFilter, TransferSchema,
)
from app.dependencies import CardServiceDep, AdminDep, CurrentUserDep

router = APIRouter(prefix="/api/cards", tags=["Cards (Admin)"])


@router.get("/", summary="Get card by query")
@handle_business_errors
def get_all_cards(
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: CardFilter = Depends()
) -> list[OwnerCardSchema]:
    return service.get(user, schema)


@router.post("/", status_code=201, summary="Add card")
@handle_business_errors
def add_card(_: AdminDep, service: CardServiceDep, schema: CardCreate) -> CardSchema:
    return service.add(schema)


@router.get("/{id}", summary="Get card by id")
@handle_business_errors
def get_all_cards(user: CurrentUserDep, service: CardServiceDep, id: int) -> list[OwnerCardSchema]:
    return service.get_by_id(user, id)


@router.delete("/{id}", status_code=204, summary="Delete card")
@handle_business_errors
def delete_card(_: AdminDep, service: CardServiceDep, id: int):
    return service.delete(id)


@router.put("/{id}", summary="Replace card")
@handle_business_errors
def replace_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardReplace) -> CardSchema:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Part update card")
@handle_business_errors
def part_update_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardPU) -> CardSchema:
    return service.part_update(id, schema)


@router.patch("/{id}/status", summary="Change card status")
@handle_business_errors
def block_card(_: AdminDep, service: CardServiceDep, id: int, new_status: CardStatus) -> OwnerCardSchema:
    return service.change_status(id, new_status)


@router.post("/{id}/transfer", summary="Transfer money from card to other card of authed user")
@handle_business_errors
def transfer_money(
        id: Annotated[int, Path(ge=1)],
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: TransferSchema,
):
    return service.money_transfer(user, id, schema)
