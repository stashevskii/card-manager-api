from decimal import Decimal
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.app.core.exceptions import (
    UserAlreadyExistsError,
    DuplicateEmailError,
    DuplicateUsernameError,
    NotFoundUserError,
    CardAlreadyExistsError,
    CardNotFoundError,
    InsufficientFundsError
)
from src.app.core.exceptions import DuplicateCardNumberError, InactiveCardError
from src.app.models import User, Card
from .enums import CardStatus


def exists(repository, **kwargs) -> bool:
    return any(all(getattr(obj, key) == value for key, value in kwargs.items()) for obj in repository.get_all())


def validate_user(
        repo,
        id: int = None,
        email: str | EmailStr = None,
        username: str = None,
        check_exists: bool = False,
        check_not_found: bool = False
) -> None:
    if check_exists:
        if id is not None and exists(repo, id=id):
            raise UserAlreadyExistsError
        if email is not None and exists(repo, email=email):
            raise DuplicateEmailError
        if username is not None and exists(repo, username=username):
            raise DuplicateUsernameError

    if check_not_found and id is not None and not exists(repo, id=id):
        raise NotFoundUserError


def validate_card(
        repo,
        id: int = None,
        number: str = None,
        check_exists: bool = False,
        check_not_found: bool = False
) -> None:
    if check_exists:
        if id is not None and exists(repo, id=id):
            raise CardAlreadyExistsError
        if number is not None and exists(repo, number=number):
            raise DuplicateCardNumberError

    if check_not_found and exists(repo, id=id) or check_not_found and not exists(repo, id=id):
        raise CardNotFoundError


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
