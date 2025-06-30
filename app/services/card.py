from app.core.base import Service
from app.models import BlockCard
from app.utils import validate_card, validate_user, validate_balance, validate_card_status
from app.models import Card, User
from app.core.exceptions import CardNotFoundError
from app.utils import validate_user_card
from app.schemas import CardCreate, CardReplace, CardPU, CardFilter, CardPagination, CardBlockSchema, TransferSchema


class CardService(Service):
    def admin_get(self, schema: CardFilter) -> list[Card]:
        response = self.repository.get(**schema.model_dump(exclude_none=True))
        if not response:
            raise CardNotFoundError
        return response

    def admin_get_by_id(self, id: int) -> Card:
        response = self.repository.get(id=id)
        if not response:
            raise CardNotFoundError
        return response

    def admin_add(self, schema: CardCreate) -> Card:
        validate_user(schema.owner_id, check_not_found=True)
        validate_card(schema.id, schema.number, check_exists=True)
        return self.repository.add(schema)

    def admin_delete(self, id: int) -> dict[str, bool]:
        validate_card(id, check_not_found=True)
        self.repository.delete(id)
        return {"success": True}

    def admin_replace(self, id: int, schema: CardReplace) -> Card:
        validate_card(id, check_not_found=True)
        validate_card(number=schema.number, check_exists=True)
        return self.repository.replace(id, schema)

    def admin_part_update(self, id: int, schema: CardPU) -> Card:
        validate_card(id, check_not_found=True)
        validate_card(number=schema.number, check_exists=True)
        return self.repository.part_update(id, schema)

    def admin_block(self, id: int) -> dict[str, bool]:
        validate_card(id, check_not_found=True)
        self.repository.block(id)
        return {"success": True}

    def admin_activate(self, id: int) -> dict[str, bool]:
        validate_card(id, check_not_found=True)
        self.repository.activate(id)
        return {"success": True}

    def admin_get_required_blocks(self) -> list[BlockCard]:
        return self.repository.get_required_blocks()

    def get(self, current_user: User, schema: CardFilter) -> list[Card]:
        response = self.repository.get(**schema.model_dump(exclude_none=True), owner_id=current_user.id)
        if not response:
            raise CardNotFoundError
        return response

    def get_all(self, current_user: User) -> list[Card]:
        response = self.repository.get(owner_id=current_user.id)
        if not response:
            raise CardNotFoundError
        return response

    def paginate(self, current_user: User, schema: CardPagination) -> list[Card]:
        response = self.repository.paginate(schema, current_user)
        if not response:
            raise CardNotFoundError
        return response

    def require_block(self, current_user: User, schema: CardBlockSchema) -> BlockCard:
        validate_user_card(current_user, schema.card_id)
        return self.repository.require_block(**schema.model_dump(), user_id=current_user.id)

    def money_transfer(self, current_user: User, schema: TransferSchema) -> dict[str, bool]:
        validate_user_card(current_user, schema.card_id)
        validate_user_card(current_user, schema.target_card_id)
        validate_card_status(schema.card_id, self.repository.session)
        validate_card_status(schema.target_card_id, self.repository.session)
        validate_balance(schema.card_id, schema.money, self.repository.session)
        self.repository.money_transfer(schema)
        return {"success": True}
