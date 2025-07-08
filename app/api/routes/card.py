from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from app.core.enums import CardStatus
from app.utils import handle_business_errors
from app.schemas import (
    CardUpdate,
    CardSchema,
    OwnerCardSchema,
    CardReplace,
    CardCreate, CardFilter, TransferSchema,
)
from app.dependencies import CardServiceDep, AdminDep, CurrentUserDep

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/", summary="Get list of cards by query. For admin all cards, own for user")
@handle_business_errors
def get_cards_by_query(
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: CardFilter = Depends()
) -> list[OwnerCardSchema]:
    return service.get(user, schema)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create card. For admin only")
@handle_business_errors
def create_card(_: AdminDep, service: CardServiceDep, schema: CardCreate) -> CardSchema:
    return service.add(schema)


@router.get("/{id}", summary="Get card by id. For admin all cards, own for user")
@handle_business_errors
def get_card_by_id(user: CurrentUserDep, service: CardServiceDep, id: int) -> OwnerCardSchema:
    return service.get_by_id(user, id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete card. For admin only")
@handle_business_errors
def delete_card(_: AdminDep, service: CardServiceDep, id: int):
    return service.delete(id)


@router.put("/{id}", summary="Replace card. For admin only")
@handle_business_errors
def replace_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardReplace) -> CardSchema:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Update card. For admin only")
@handle_business_errors
def update_card(_: AdminDep, service: CardServiceDep, id: int, schema: CardUpdate) -> CardSchema:
    return service.update(id, schema)


@router.patch("/{id}/status", summary="Change card status. For admin only")
@handle_business_errors
def block_card(_: AdminDep, service: CardServiceDep, id: int, new_status: CardStatus) -> OwnerCardSchema:
    return service.change_status(id, new_status)


@router.post("/{id}/transfer", summary="Transfer money from one user card to another")
@handle_business_errors
def transfer_money(
        id: Annotated[int, Path(ge=1)],
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: TransferSchema,
):
    return service.money_transfer(user, id, schema)
