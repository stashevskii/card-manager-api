from sqlalchemy.orm import joinedload
from app.enums import CardStatus
from app.repositories.abstract import AbstractRepository
from app.schemas import TransferSchema
from app.models import Card


class CardRepository(AbstractRepository[Card]):
    def get(self, **kwargs) -> list[Card]:
        data = {k: v for k, v in kwargs.items() if k not in ("skip", "limit")}
        return self.session.query(
            self.table
        ).options(
            joinedload(Card.owner)
        ).filter_by(**data).offset(kwargs.get("skip")).limit(kwargs.get("limit")).all()

    def change_status(self, id: int, new_status: CardStatus) -> Card:
        card = self.session.query(self.table).filter_by(id=id).first()
        card.status = new_status
        self.commit()
        return card

    def money_transfer(self, id: int, schema: TransferSchema) -> None:
        try:
            card = self.session.query(self.table).filter_by(id=id).first()
            target_card = self.session.query(self.table).filter_by(id=schema.target_card_id).first()
            card.balance -= schema.money
            target_card.balance += schema.money
            self.commit()
        except Exception:
            self.session.rollback()
