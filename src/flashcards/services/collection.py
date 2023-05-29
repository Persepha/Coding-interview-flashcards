from typing import Iterable

from sqlalchemy import select
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


collection_crud = CRUDCollection(Collection)
