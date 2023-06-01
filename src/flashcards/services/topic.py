from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from common.services import CRUDBase
from flashcards.models.flashcard import Collection
from flashcards.models.topic import Topic
from flashcards.schemas.topic_schemas import TopicCreateModel, TopicUpdateModel


class CRUDTopic(CRUDBase[Topic, TopicCreateModel, TopicUpdateModel]):
    async def get_list_with_collections(
        self, *, session: AsyncSession
    ) -> Iterable[Topic]:
        query = (
            select(Topic)
            .options(joinedload(Topic.collections).subqueryload(Collection.flashcards))
            .options(joinedload(Topic.collections).subqueryload(Collection.creator))
        )

        topics = await session.execute(query)

        return topics.scalars().unique().all()

    async def get_by_id(self, *, session: AsyncSession, id: int) -> Topic:
        query = (
            select(Topic)
            .options(joinedload(Topic.collections).subqueryload(Collection.flashcards))
            .options(joinedload(Topic.collections).subqueryload(Collection.creator))
            .where(Topic.id == id)
        )

        topic = await session.execute(query)

        return topic.scalar()


topic_crud = CRUDTopic(Topic)
