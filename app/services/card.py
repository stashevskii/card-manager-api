from fastapi import Response, status
from app.core.base import Service
from app.enums import UserRole, CardStatus
from app.utils import validate_card, validate_user, validate_balance, validate_card_status
from app.models import Card, User
from app.core.exceptions import CardNotFoundError
from app.utils import validate_user_card
from app.schemas import CardCreate, CardReplace, CardPU, CardFilter, TransferSchema


class CardService(Service):
    @staticmethod
    def __get_query_by_role(user: User, **kwargs) -> dict:
        return kwargs | {"owner_id": user.id} if user.role == UserRole.USER else kwargs

    def get(self, user: User, schema: CardFilter) -> list[Card]:
        response = self.repository.get(**self.__get_query_by_role(user, **schema.model_dump(exclude_none=True)))
        if not response:
            raise CardNotFoundError
        return response

    def get_by_id(self, user: User, id: int) -> Card:
        response = self.repository.get(**self.__get_query_by_role(user, id=id))
        if not response:
            raise CardNotFoundError
        return response

    def add(self, schema: CardCreate) -> Card:
        validate_user(schema.owner_id, check_not_found=True)
        validate_card(schema.id, schema.number, check_exists=True)
        return self.repository.add(schema)

    def delete(self, id: int) -> dict[str, bool]:
        validate_card(id, check_not_found=True)
        self.repository.delete(id)

    def replace(self, id: int, schema: CardReplace) -> Card:
        validate_card(id, check_not_found=True)
        validate_card(number=schema.number, check_exists=True)
        return self.repository.replace(id, schema)

    def part_update(self, id: int, schema: CardPU) -> Card:
        validate_card(id, check_not_found=True)
        validate_card(number=schema.number, check_exists=True)
        return self.repository.part_update(id, schema)

    def change_status(self, id: int, new_status: CardStatus) -> dict[str, bool]:
        validate_card(id, check_not_found=True)
        return self.repository.change_status(id, new_status)

    def money_transfer(self, current_user: User, id: int, schema: TransferSchema) -> dict[str, bool]:
        validate_user_card(current_user, id)
        validate_user_card(current_user, schema.target_card_id)
        validate_card_status(id, self.repository.session)
        validate_card_status(schema.target_card_id, self.repository.session)
        validate_balance(id, schema.money, self.repository.session)
        self.repository.money_transfer(id, schema)
        return {"success": True}
