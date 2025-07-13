from app.core.base import BaseSchema
from app.models import BlockRequest, User
from app.repositories.abstract import AbstractRepository


class BlockRequestRepository(AbstractRepository[BlockRequest]):
    def create(self, user: User, schema: BaseSchema) -> BlockRequest:
        entity = self.table(**schema.model_dump(exclude_none=True), user=user)
        self.session.add(entity)
        self.commit()
        return entity
