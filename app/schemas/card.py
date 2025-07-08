from datetime import date
from decimal import Decimal
from typing import Optional, Any
from pydantic import Field, field_validator
from app.core.base import BaseSchema
from app.enums import CardStatus
from .lite import UserLite


class OwnerMixin(BaseSchema):
    owner: UserLite


class CardBase(BaseSchema):
    number: str = Field(min_length=16, max_length=16)
    status: CardStatus
    balance: Decimal
    expired_at: date


class OCardBase(BaseSchema):
    number: Optional[str] = Field(None, min_length=16, max_length=16)
    status: Optional[CardStatus] = None
    balance: Optional[Decimal] = None
    expired_at: Optional[date] = None


class CardSchema(CardBase):
    @field_validator("number", mode="before")
    @classmethod
    def mask_card_number(cls, v: Any) -> str:
        return "************" + v[-4:]

    id: int = Field(ge=1)


class CardFilter(OCardBase):
    id: Optional[int] = Field(None, ge=1)
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)


class CardUpdate(OCardBase):
    ...


class CardReplace(CardBase):
    ...


class CardCreate(CardBase):
    owner_id: int = Field(ge=1)
    id: Optional[int] = Field(None, ge=1)


class OwnerCardSchema(CardSchema, OwnerMixin):
    ...


class CardBlockSchema(BaseSchema):
    card_id: int = Field(ge=1)
    message: str = Field(max_length=50)


class CardBlockResponse(BaseSchema):
    card_id: int = Field(ge=1)
    message: str = Field(max_length=50)
    user: UserLite


class TransferSchema(BaseSchema):
    target_card_id: int = Field(ge=1)
    money: Decimal = Field(ge=0.01)
