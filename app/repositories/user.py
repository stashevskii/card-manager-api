from app.core.base import Repository
from app.schemas import UserCreate
from app.models import User


class UserRepository(Repository[User]):
    def get(self, **kwargs) -> User:
        return self.session.query(self.table).filter_by(**kwargs).first()

    def add(self, schema: UserCreate) -> User:
        user = self.table(**schema.model_dump(exclude_none=True))
        self.session.add(user)
        self.commit()
        return user

    def delete(self, id: int) -> None:
        user = self.session.query(self.table).filter_by(id=id).first()
        self.session.delete(user)
        self.commit()

    def __update(self, id: int, **kwargs) -> User:
        user = self.session.query(self.table).filter_by(id=id).first()
        for k, v in kwargs.items():
            setattr(user, k, v)
        self.commit()
        return user

    def replace(self, id: int, **kwargs) -> User:
        return self.__update(id, **kwargs)

    def part_update(self, id: int, **kwargs) -> User:
        return self.__update(id, **kwargs)
