from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from common.dependencies import get_obj_or_404
from common.services import CRUDBase
from flashcards.models.flashcard import Collection
from flashcards.models.topic import Topic
from flashcards.schemas.collection_schemas import (CollectionCreateModel,
                                                   CollectionUpdateModel)
from flashcards.services.flashcard import flashcard_crud


class CRUDCollection(
    CRUDBase[Collection, CollectionCreateModel, CollectionUpdateModel]
):
    async def get_list(self, *, session: AsyncSession) -> Iterable[Collection]:
        query = select(Collection).options(
            joinedload(Collection.flashcards),
            joinedload(Collection.creator),
            joinedload(Collection.topic),
        )
        collection_list = await session.execute(query)

        return collection_list.scalars().unique().all()

    async def get_collection_by_id(
        self, *, id: int, session: AsyncSession
    ) -> Collection:
        query = (
            select(Collection)
            .options(
                joinedload(Collection.flashcards),
                joinedload(Collection.creator),
                joinedload(Collection.topic),
            )
            .where(Collection.id == id)
        )

        collection = await session.execute(query)

        return collection.scalar()

    async def create_with_flashcards(
        self,
        *,
        session: AsyncSession,
        create_dto: CollectionUpdateModel,
        creator_id: int
    ) -> Collection:
        data = create_dto.dict()

        topic_id = data.pop("topic_id")
        topic = await get_obj_or_404(session=session, id=topic_id, obj=Topic)

        flashcards_ids = data.pop("flashcards_ids")

        new_collection = Collection(**data, creator_id=creator_id, topic_id=topic_id)

        if flashcards_ids is not None:
            flashcards = await flashcard_crud.get_flashcards_by_ids(
                session=session, flashcards_ids=flashcards_ids
            )
            new_collection.flashcards = flashcards

        session.add(new_collection)
        await session.commit()

        return new_collection

    async def update(
        self,
        *,
        session: AsyncSession,
        collection: Collection,
        collection_update_dto: CollectionUpdateModel
    ):
        data = collection_update_dto.dict(exclude_unset=True)

        flashcards_ids = data.pop("flashcards_ids", None)
        topic_id = data.pop("topic_id", None)

        for field in data:
            if getattr(collection, field) != data[field]:
                setattr(collection, field, data[field])

        if flashcards_ids is not None:
            flashcards = await flashcard_crud.get_flashcards_by_ids(
                session=session, flashcards_ids=flashcards_ids
            )
            collection.flashcards = flashcards

        if topic_id is not None:
            topic = await get_obj_or_404(session=session, id=topic_id, obj=Topic)
            collection.topic_id = topic_id

        await session.commit()

        return collection


collection_crud = CRUDCollection(Collection)
