from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only, selectinload

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

    async def get_preview_by_id(self, *, session: AsyncSession, id: int) -> Topic:
        # query = (
        #     select(Topic).options(joinedload(Topic.collections)).where(Topic.id == id)
        # )

        query = (
            select(Topic)
            .options(
                selectinload(Topic.collections).load_only(
                    Collection.id, Collection.name
                )
            )
            .where(Topic.id == id)
        )

        topic = await session.execute(query)

        return topic.scalar()


topic_crud = CRUDTopic(Topic)
