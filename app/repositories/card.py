from sqlalchemy.orm import joinedload
from app.core.base import Repository
from app.enums import CardStatus
from app.schemas import CardReplace, CardPU, CardCreate, TransferSchema
from app.models import Card


class CardRepository(Repository[Card]):
    def get(self, **kwargs) -> list[Card]:
        data = {k: v for k, v in kwargs.items() if k not in ("skip", "limit")}
        return self.session.query(
            self.table
        ).options(
            joinedload(Card.owner)
        ).filter_by(**data).offset(kwargs.get("skip")).limit(kwargs.get("limit")).all()

    def add(self, schema: CardCreate) -> Card:
        card = self.table(**schema.model_dump())
        self.session.add(card)
        self.commit()
        return card

    def delete(self, id: int) -> None:
        card = self.session.query(self.table).filter_by(id=id).first()
        self.session.delete(card)
        self.commit()

    def __update(self, id: int, schema: dict) -> Card:
        card = self.session.query(self.table).filter_by(id=id).first()
        for k, v in schema.items():
            setattr(card, k, v)
        self.commit()
        return card

    def replace(self, id: int, schema: CardReplace) -> Card:
        return self.__update(id, schema.model_dump())

    def part_update(self, id: int, schema: CardPU) -> Card:
        return self.__update(id, schema.model_dump(exclude_none=True))

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
