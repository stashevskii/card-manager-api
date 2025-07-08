from app.core.base import Repository, BaseSchema


class AbstractRepository[T](Repository[T]):
    def add(self, schema: BaseSchema) -> T:
        entity = self.table(**schema.model_dump(exclude_none=True))
        self.session.add(entity)
        self.commit()
        return entity

    def delete(self, id: int) -> None:
        entity = self.session.query(self.table).filter_by(id=id).first()
        self.session.delete(entity)
        self.commit()

    def __update(self, id: int, **kwargs) -> T:
        entity = self.session.query(self.table).filter_by(id=id).first()
        for k, v in kwargs.items():
            setattr(entity, k, v)
        self.commit()
        return entity

    # put http method
    def replace(self, id: int, schema: BaseSchema) -> T:
        return self. __update(id, **schema.model_dump())

    # patch http method
    def update(self, id: int, schema: BaseSchema) -> T:
        return self. __update(id, **schema.model_dump(exclude_none=True))
