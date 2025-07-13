from typing import Optional
from pydantic import Field

from app.core.base import BaseSchema
from .lite import CardLite, UserLite


class BlockRequestBase(BaseSchema):
    message: str = Field(min_length=10)
    card_id: int = Field(ge=1)


class OBlockRequestBase(BaseSchema):
    message: Optional[str] = Field(None, min_length=10)
    card_id: Optional[int] = Field(None, ge=1)


class BlockRequestFilter(OBlockRequestBase):
    id: Optional[int] = Field(None, ge=1)


class BlockRequestCreate(BlockRequestBase):
    id: Optional[int] = Field(None, ge=1)


class BlockRequestResponse(BaseSchema):
    id: int = Field(ge=1)
    message: str
    card: CardLite
    user: UserLite


class BlockRequestUpdate(OBlockRequestBase):
    ...


class BlockRequestReplace(BlockRequestBase):
    ...
