from datetime import date
from decimal import Decimal
from typing import Any
from pydantic import EmailStr, Field, field_validator
from src.app.core.base import BaseSchema
from src.app.core.utils import CardStatus, UserRole


class UserLite(BaseSchema):
    id: int = Field(ge=1)
    username: str = Field(max_length=30)
    email: EmailStr
    role: UserRole


class CardLite(BaseSchema):
    id: int = Field(ge=1)
    number: str = Field(min_length=16, max_length=16)

    @field_validator("number", mode="before")
    @classmethod
    def mask_card_number(cls, v: Any) -> str:
        return "************" + v[-4:]

    status: CardStatus
    balance: Decimal
    expired_at: date
