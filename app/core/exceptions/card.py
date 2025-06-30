class CardNotFoundError(Exception):
    ...


class CardAlreadyExistsError(Exception):
    ...


class DuplicateCardNumberError(Exception):
    ...


class InsufficientFundsError(Exception):
    ...


class InactiveCardError(Exception):
    ...
