from fastapi import APIRouter, Depends
from app.dependencies import CurrentUserDep, CardServiceDep
from app.utils import handle_business_errors
from app.schemas import CardSchema, CardFilter, CardPagination, CardBlockSchema, CardBlockResponse, TransferSchema

router = APIRouter(prefix="/api/cards", tags=["Cards (User)"])


@router.get("/", summary="Search for authed user's cards")
@handle_business_errors
def get_user_cards(user: CurrentUserDep, service: CardServiceDep, schema: CardFilter = Depends()) -> list[CardSchema]:
    return service.get_user_cards(user, schema)


@router.get("/all", summary="Get all cards of authed user")
@handle_business_errors
def get_all_user_cards(user: CurrentUserDep, service: CardServiceDep) -> list[CardSchema]:
    return service.get_all_user_cards(user)


@router.get("/paginate", summary="Pagination on all cards of authed user")
@handle_business_errors
def paginate_user_cards(
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: CardPagination = Depends()
) -> list[CardSchema]:
    return service.paginate(user, schema)


@router.post("/block-request", summary="Require block of card of authed user")
@handle_business_errors
def require_card_block(
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: CardBlockSchema = Depends()
) -> CardBlockResponse:
    return service.require_block(user, schema)


@router.post("/transfer", summary="Transfer money from card to other card of authed user")
@handle_business_errors
def transfer_money(
        user: CurrentUserDep,
        service: CardServiceDep,
        schema: TransferSchema = Depends(),
):
    return service.money_transfer(user, schema)
