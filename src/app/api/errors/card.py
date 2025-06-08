from fastapi import HTTPException, status


class HTTPNotFoundCard(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
            headers=None
        )


class HTTPCardAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card already exists",
            headers=None
        )


class HTTPDuplicateCardNumber(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card with this number already exists",
            headers=None
        )


class HTTPInactiveCard(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive card",
            headers=None
        )


class HTTPInsufficientFunds(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough money",
            headers=None
        )
