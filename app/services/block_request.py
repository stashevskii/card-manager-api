from app.core.base import BaseSchema
from app.core.exceptions import BlockRequestNotFoundError, BlockRequestAlreadyExistsError
from app.models import BlockRequest, User
from app.schemas import BlockRequestCreate
from app.services.abstract import AbstractService
from app.utils import validate_user_card, validate_card
from app.utils.validation import validate_block_request


class BlockRequestService(AbstractService[BlockRequest]):
    def __init__(self, repository):
        super().__init__(
            repository,
            BlockRequest,
            BlockRequestNotFoundError,
            BlockRequestAlreadyExistsError
        )

    def create(self, user: User, schema: BlockRequestCreate) -> BlockRequest:
        validate_user_card(user, schema.card_id)
        validate_block_request(schema.card_id)
        return self.repository.create(user, schema)

    def replace(self, id: int, schema: BaseSchema) -> BlockRequest:
        validate_card(id, check_exists=True)
        return super().replace(id, schema)

    def update(self, id: int, schema: BaseSchema) -> BlockRequest:
        validate_card(id, check_exists=True)
        return super().update(id, schema)
