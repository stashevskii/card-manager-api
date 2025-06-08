from functools import wraps
from typing import Callable, Any
from src.app.api.errors import (
    HTTPUserNotFound,
    HTTPUserAlreadyExists,
    HTTPDuplicateEmail,
    HTTPDuplicateUsername,
    HTTPNotFoundCard,
    HTTPCardAlreadyExists,
    HTTPDuplicateCardNumber,
    HTTPInactiveCard,
    HTTPInsufficientFunds
)
from src.app.core.exceptions import (
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
    NotFoundUserError: HTTPUserNotFound,
    UserAlreadyExistsError: HTTPUserAlreadyExists,
    DuplicateUsernameError: HTTPDuplicateUsername,
    DuplicateEmailError: HTTPDuplicateEmail,
    CardNotFoundError: HTTPNotFoundCard,
    CardAlreadyExistsError: HTTPCardAlreadyExists,
    DuplicateCardNumberError: HTTPDuplicateCardNumber,
    InactiveCardError: HTTPInactiveCard,
    InsufficientFundsError: HTTPInsufficientFunds
}


def handle_business_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            try:
                raise BUSINESS2HTTP[e.__class__]
            except KeyError:
                return

    return wrapper
