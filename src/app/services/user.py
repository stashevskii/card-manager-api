from src.app.core.base import Service
from src.app.core.utils import validate_user, hash_password
from src.app.core.exceptions import NotFoundUserError
from src.app.schemas import UserFilter, UserCreate, UserReplace, UserPU
from src.app.models import User


class UserService(Service):
    def admin_get(self, schema: UserFilter) -> User:
        response = self.repository.get(schema)
        if response is None:
            raise NotFoundUserError
        return response

    def admin_add(self, schema: UserCreate) -> User:
        validate_user(self.repository, schema.id, schema.email, schema.username, check_exists=True)
        schema.password = hash_password(schema.password)
        return self.repository.add(schema)

    def admin_delete(self, id: int) -> dict[str, bool]:
        validate_user(self.repository, id, check_not_found=True)
        self.repository.delete(id)
        return {"success": True}

    def admin_replace(self, id: int, schema: UserReplace) -> User:
        validate_user(self.repository, id, check_not_found=True)
        validate_user(
            self.repository,
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        schema.password = hash_password(schema.password)
        return self.repository.replace(id, **schema.model_dump())

    def admin_part_update(self, id: int, schema: UserPU) -> User:
        validate_user(self.repository, id, check_not_found=True)
        validate_user(
            self.repository,
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        if schema.password is not None:
            schema.password = hash_password(schema.password)
        return self.repository.part_update(id, schema.model_dump(exclude_none=True))
