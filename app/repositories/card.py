from app.core.base import Repository
from app.enums import CardStatus
from app.schemas import CardReplace, CardPU, CardCreate, CardPagination, TransferSchema
from app.models import Card, User, BlockCard


class CardRepository(Repository[Card]):
    def get(self, **kwargs) -> list[Card]:
        return self.session.query(self.table).filter_by(**kwargs).all()

    def paginate(self, schema: CardPagination, user: User) -> list[Card]:
        return self.session.query(self.table).filter_by(owner_id=user.id).offset(schema.skip).limit(schema.limit).all()

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

    def block(self, id: int) -> None:
        card = self.session.query(self.table).filter_by(id=id).first()
        card.status = CardStatus.BLOCKED
        self.commit()

    def activate(self, id: int) -> None:
        card = self.session.query(self.table).filter_by(id=id).first()
        card.status = CardStatus.ACTIVE
        self.commit()

    def require_block(self, **kwargs) -> BlockCard:
        block_request = BlockCard(**kwargs)
        self.session.add(block_request)
        self.commit()
        return block_request

    def get_required_blocks(self) -> list[BlockCard]:
        return self.session.query(BlockCard).all()

    def money_transfer(self, schema: TransferSchema) -> None:
        try:
            card = self.session.query(self.table).filter_by(id=schema.card_id).first()
            target_card = self.session.query(self.table).filter_by(id=schema.target_card_id).first()
            card.balance -= schema.money
            target_card.balance += schema.money
            self.commit()
        except Exception:
            self.session.rollback()
