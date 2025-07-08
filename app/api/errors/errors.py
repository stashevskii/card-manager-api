from fastapi import HTTPException, status

from app.core.exceptions import (
    NotFoundUserError,
    UserAlreadyExistsError,
    DuplicateUsernameError,
    DuplicateEmailError,
    CardNotFoundError,
    CardAlreadyExistsError,
    DuplicateCardNumberError,
    InactiveCardError,
    InsufficientFundsError
)

BUSINESS2HTTP = {
    NotFoundUserError: HTTPException(status.HTTP_404_NOT_FOUND, "User not found"),
    UserAlreadyExistsError: HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists"),
    DuplicateUsernameError: HTTPException(status.HTTP_400_BAD_REQUEST, "User with this username already exists"),
    DuplicateEmailError: HTTPException(status.HTTP_400_BAD_REQUEST, "User with this email already exists"),
    CardNotFoundError: HTTPException(status.HTTP_404_NOT_FOUND, "Card not found"),
    CardAlreadyExistsError: HTTPException(status.HTTP_400_BAD_REQUEST, "Card already exists"),
    DuplicateCardNumberError: HTTPException(status.HTTP_400_BAD_REQUEST, "Card with this number already exists"),
    InactiveCardError: HTTPException(status.HTTP_400_BAD_REQUEST, "Inactive card"),
    InsufficientFundsError: HTTPException(status.HTTP_400_BAD_REQUEST, "Not enough money")
}
