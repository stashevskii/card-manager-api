from app.core.base import Service
from app.utils import validate_user, hash_password
from app.core.exceptions import NotFoundUserError
from app.schemas import UserFilter, UserCreate, UserReplace, UserPU
from app.models import User


class UserService(Service):
    def get_by_id(self, id: int) -> User:
        response = self.repository.get(id=id)
        if not response:
            raise NotFoundUserError
        return response[0]

    def get(self, schema: UserFilter) -> User:
        response = self.repository.get(**schema.model_dump(exclude_none=True))
        if not response:
            raise NotFoundUserError
        return response

    def add(self, schema: UserCreate) -> User:
        validate_user(schema.id, schema.email, schema.username, check_exists=True)
        schema.password = hash_password(schema.password)
        return self.repository.add(schema)

    def delete(self, id: int) -> dict[str, bool]:
        validate_user(id, check_not_found=True)
        self.repository.delete(id)

    def replace(self, id: int, schema: UserReplace) -> User:
        validate_user(id, check_not_found=True)
        validate_user(
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        schema.password = hash_password(schema.password)
        return self.repository.replace(id, **schema.model_dump())

    def part_update(self, id: int, schema: UserPU) -> User:
        validate_user(id, check_not_found=True)
        validate_user(
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        if schema.password is not None:
            schema.password = hash_password(schema.password)
        return self.repository.part_update(id, schema.model_dump(exclude_none=True))
