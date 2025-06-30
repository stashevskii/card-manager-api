from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base import Base


class BlockCard(Base):
    __tablename__ = "required_card_blocks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(50), nullable=False)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.id"))
    card: Mapped["Card"] = relationship("Card")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"BlockCard(id={self.id}, message={self.message}, card_id={self.card_id}, user_id={self.user_id})"
