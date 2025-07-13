from sqlalchemy.orm import joinedload
from app.models import User
from app.repositories.abstract import AbstractRepository
from app.schemas import UserCreate


class UserRepository(AbstractRepository[User]):
    def get(self, **kwargs) -> list[User]:
        return self.session.query(self.table).options(joinedload(User.cards)).filter_by(**kwargs).all()
