from decimal import Decimal
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.core.exceptions import (
    UserAlreadyExistsError,
    DuplicateEmailError,
    DuplicateUsernameError,
    NotFoundUserError,
    CardAlreadyExistsError,
    CardNotFoundError,
    InsufficientFundsError
)
from app.core.exceptions import DuplicateCardNumberError, InactiveCardError
from app.models import User, Card
from app.core.base import Base
from app.enums import CardStatus
from app.core.db import get_db


def exists(table: type[Base], **kwargs) -> bool:
    db = next(get_db())
    return db.query(table).filter_by(**kwargs).first() is not None


def validate_entity_by_id(id: int, table: type[Base], e: Exception, check_exists: bool = False):
    entity_exists = exists(table, id=id)
    if (entity_exists and check_exists) or (not entity_exists and not check_exists):
        raise e


def validate_user(
        id: int = None,
        email: str | EmailStr = None,
        username: str = None,
        check_exists: bool = False,
        check_not_found: bool = False
) -> None:
    if check_exists:
        if id is not None and exists(User, id=id):
            raise UserAlreadyExistsError
        if email is not None and exists(User, email=email):
            raise DuplicateEmailError
        if username is not None and exists(User, username=username):
            raise DuplicateUsernameError

    if check_not_found and id is not None and not exists(User, id=id):
        raise NotFoundUserError


def validate_card(
        id: int = None,
        number: str = None,
        check_exists: bool = False,
        check_not_found: bool = False
) -> None:
    if check_exists:
        if id is not None and exists(Card, id=id):
            raise CardAlreadyExistsError
        if number is not None and exists(Card, number=number):
            raise DuplicateCardNumberError

    if check_not_found:
        if id is not None and not exists(Card, id=id):
            raise CardNotFoundError
        if number is not None and not exists(Card, number=number):
            raise DuplicateCardNumberError


def validate_user_card(user: User, card_id: int) -> None:
    for card in user.cards:
        if card.id == card_id:
            return
    raise CardNotFoundError


def validate_balance(card_id: int, money: Decimal, db: Session) -> None:
    card = db.query(Card).filter_by(id=card_id).first()
    if card.balance < money:
        raise InsufficientFundsError


def validate_card_status(card_id: int, db: Session) -> None:
    card = db.query(Card).filter_by(id=card_id).first()
    if card.status != CardStatus.ACTIVE:
        raise InactiveCardError
