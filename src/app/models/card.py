from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, Enum as SQLAlchemyEnum, ForeignKey, event
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.orm.context import QueryContext
from src.app.core.base import Base
from src.app.core.utils import CardStatus


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="cards"
    )
    status: Mapped[CardStatus] = mapped_column(
        SQLAlchemyEnum(CardStatus, native_enum=False, length=20),
        default=CardStatus.ACTIVE
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), nullable=False)
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"Card(id={self.id}, number={self.number}, balance={self.balance}, expired_at={self.expired_at})"


@event.listens_for(Card, "load")
def check_expired(target: Card, _: QueryContext) -> None:
    if datetime.today() >= target.expired_at:
        target.status = CardStatus.EXPIRED
