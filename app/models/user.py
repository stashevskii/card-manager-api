from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base import Base
from app.core.enums import UserRole


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)  # hashed, but str
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    cards: Mapped[list["Card"]] = relationship(
        "Card",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, native_enum=False, length=20),
        default=UserRole.USER
    )

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
