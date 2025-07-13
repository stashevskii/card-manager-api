from sqlalchemy.orm import Session


class Repository[T]:
    def __init__(self, session: Session, table: type[T]):
        self.session = session
        self.table = table

    def commit(self) -> None:
        self.session.commit()
