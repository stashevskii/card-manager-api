from app.core.base import Service, BaseSchema
from app.utils.validation import validate_entity_by_id


class AbstractService[T](Service):
    def __init__(self, repository, table: T, not_found_error, already_exists_error: Exception):
        super().__init__(repository)
        self.table = table
        self.not_found_error = not_found_error
        self.already_exists_error = already_exists_error

    def get_by_id(self, id: int) -> T:
        response = self.repository.get(id=id)
        if not response:
            raise self.not_found_error
        return response[0]

    def get(self, schema: BaseSchema) -> T:
        response = self.repository.get(**schema.model_dump(exclude_none=True))
        if not response:
            raise self.not_found_error
        return response

    def create(self, schema: BaseSchema) -> T:
        validate_entity_by_id(schema.id, self.table, self.not_found_error, True)
        return self.repository.create(schema)

    def delete(self, id: int):
        validate_entity_by_id(id, self.table, self.not_found_error)
        self.repository.delete(id)

    def replace(self, id: int, schema: BaseSchema) -> T:
        validate_entity_by_id(id, self.table, self.not_found_error)
        return self.repository.replace(id, schema)

    def update(self, id: int, schema: BaseSchema) -> T:
        validate_entity_by_id(id, self.table, self.not_found_error)
        return self.repository.update(id, schema)
