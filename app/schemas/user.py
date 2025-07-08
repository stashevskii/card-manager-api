from typing import Optional
from pydantic import Field, EmailStr
from app.core.base import BaseSchema
from app.enums import UserRole
from .lite import CardLite


class UserBase(BaseSchema):
    username: str = Field(max_length=30)
    email: EmailStr
    role: UserRole


class PasswordMixin(BaseSchema):
    password: str | bytes


class OPasswordMixin(BaseSchema):
    password: Optional[str | bytes] = None


class OUserBase(BaseSchema):
    username: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class UserSchema(UserBase):
    id: int = Field(ge=1)
    cards: list[CardLite] = []


class UserFilter(OUserBase):
    id: Optional[int] = Field(None, ge=1)


class UserCreate(UserBase, PasswordMixin):
    id: Optional[int] = Field(None, ge=1)


class UserReplace(UserBase, PasswordMixin):
    ...


class UserUpdate(OUserBase, OPasswordMixin):
    ...
