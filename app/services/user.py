from app.services.abstract import AbstractService
from app.utils import validate_user, hash_password
from app.schemas import UserCreate, UserReplace, UserUpdate
from app.models import User
from app.core.exceptions import NotFoundUserError, UserAlreadyExistsError


class UserService(AbstractService[User]):
    def __init__(self, repository):
        super().__init__(repository, User, NotFoundUserError, UserAlreadyExistsError)

    def create(self, schema: UserCreate) -> User:
        print("W")
        validate_user(schema.id, schema.email, schema.username, check_exists=True)
        schema.password = hash_password(schema.password)
        return self.repository.create(schema)

    def replace(self, id: int, schema: UserReplace) -> User:
        validate_user(id, check_not_found=True)
        validate_user(
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        schema.password = hash_password(schema.password)
        return self.repository.replace(id, schema)

    def update(self, id: int, schema: UserUpdate) -> User:
        validate_user(id, check_not_found=True)
        validate_user(
            email=schema.email,
            username=schema.username,
            check_exists=True
        )
        if schema.password is not None:
            schema.password = hash_password(schema.password)
        return self.repository.update(id, schema)
