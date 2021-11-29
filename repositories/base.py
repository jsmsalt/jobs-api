from sqlmodel import Session, func, text, SQLModel, select
from typing import Any, List, Literal, Optional, Type, TypeVar, Generic

ReadType = TypeVar("ReadType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=SQLModel)
UpdateType = TypeVar("UpdateType", bound=SQLModel)


class BaseRepository(Generic[ReadType, CreateType, UpdateType]):
    entity: Type[ReadType]

    def __init__(self, db: Session):
        self.db = db

    def get_entity(self, *args: Any, **kwargs: Any) -> Optional[ReadType]:
        result = self.db.exec(
            select(self.entity)
            .filter(*args)
            .filter_by(**kwargs)
        )

        return result.first()

    def get_entities(self, *args: Any, offset: int = 0, limit: int = 100, order_by: str = 'id', order: Literal['desc', 'asc'] = 'asc', **kwargs: Any) -> List[ReadType]:
        result = self.db.exec(
            select(self.entity)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
            .order_by(text(f"{order_by} {order}"))
        )

        return result.all()

    def count_entities(self) -> int:
        return self.db.query(func.count(self.entity.id)).scalar()

    def create_entity(self, entity: CreateType) -> ReadType:
        entity = self.entity.from_orm(entity)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def create_entities(self, entities: List[CreateType]) -> ReadType:
        entities_input = []

        for entity in entities:
            entity = self.entity.from_orm(entity)
            entities_input.append(entity)

        self.db.add_all(entities_input)
        self.db.commit()

        entities_output = []

        for entity in entities:
            self.db.refresh(entity)
            entities_output.append(entity)

        return entities_output

    def delete_entity(self, *args, **kwargs) -> bool:
        try:
            entity = self.get_entity(*args, **kwargs)

            if entity is None:
                return False

            self.db.delete(entity)
            self.db.commit()

            return True
        except Exception:
            return False

    def delete_entities(self, *args, **kwargs) -> bool:
        try:
            entities = self.get_entities(*args, **kwargs)

            if entities is None:
                return False

            for entity in entities:
                self.db.delete(entity)

            self.db.commit()

            return True
        except Exception:
            return False

    def update_entity(self, data: UpdateType, *args, **kwargs) -> ReadType:
        entity = self.get_entity(*args, **kwargs)

        if entity is None:
            return None

        data = data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(entity, key, value)

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return entity

    def update_entities(self, data: UpdateType, *args, **kwargs) -> ReadType:
        entities = self.get_entities(*args, **kwargs)

        if entities is None:
            return None

        data = data.dict(exclude_unset=True)

        for entity in entities:
            for key, value in data.items():
                setattr(entity, key, value)

            self.db.add(entity)

        self.db.commit()

        for entity in entities:
            self.db.refresh(entity)

        return entities

    def update_entity_changes(self, entity: ReadType) -> ReadType:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return entity
