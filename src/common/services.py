from typing import Generic, Iterable, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.types import CreateSchemaType, ModelType, UpdateSchemaType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get_by_id(self, *, session: AsyncSession, id: int) -> ModelType:
        query = select(self.model).where(self.model.id == id)
        result = await session.execute(query)

        return result.scalar()

    async def get_list(self, *, session: AsyncSession) -> Iterable[ModelType]:
        query = select(self.model).order_by(self.model.id)
        result = await session.execute(query)

        return result.scalars().all()

    async def create(
        self, *, session: AsyncSession, create_dto: CreateSchemaType
    ) -> ModelType:
        data = create_dto.dict()
        new_db_obj = self.model(**data)

        session.add(new_db_obj)
        await session.commit()

        return new_db_obj

    async def delete(self, *, session: AsyncSession, obj: ModelType) -> ModelType:
        await session.delete(obj)
        await session.commit()

        return obj

    async def update(
        self, *, session: AsyncSession, obj: ModelType, update_dto: UpdateSchemaType
    ) -> ModelType:
        data = update_dto.dict(exclude_unset=True)

        for field in data:
            if getattr(obj, field) != data[field]:
                setattr(obj, field, data[field])

        await session.commit()

        return obj
