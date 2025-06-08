from src.app.core.base import Repository
from src.app.schemas import UserFilter, UserCreate
from src.app.models import User


class UserRepository(Repository[User]):
    def get(self, schema: UserFilter) -> type[User]:
        return self.session.query(self.table).filter_by(**schema.model_dump(exclude_none=True)).first()

    def add(self, schema: UserCreate) -> User:
        user = self.table(**schema.model_dump(exclude_none=True))
        self.session.add(user)
        self.commit()
        return user

    def delete(self, id: int) -> None:
        user = self.session.query(self.table).filter_by(id=id).first()
        self.session.delete(user)
        self.commit()

    def __update(self, id: int, **kwargs) -> User | None:
        user = self.session.query(self.table).filter_by(id=id).first()
        for k, v in kwargs.items():
            setattr(user, k, v)
        self.commit()
        return user

    def replace(self, id: int, **kwargs) -> User:
        return self.__update(id, **kwargs)

    def part_update(self, id: int, **kwargs) -> User:
        return self.__update(id, **kwargs)
