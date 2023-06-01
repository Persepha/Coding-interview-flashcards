from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.dependencies import get_obj_or_404
from database import get_async_session
from flashcards.models.flashcard import Collection, Flashcard
from flashcards.models.tag import Tag
from flashcards.models.topic import Topic


async def valid_flashcard_id(
    *, id: int, session: AsyncSession = Depends(get_async_session)
) -> Flashcard:
    flashcard = await get_obj_or_404(id=id, session=session, obj=Flashcard)

    return flashcard


async def valid_tag_id(
    *, id: int, session: AsyncSession = Depends(get_async_session)
) -> Tag:
    tag = await get_obj_or_404(id=id, session=session, obj=Tag)

    return tag


async def valid_topic_id(
    *, id: int, session: AsyncSession = Depends(get_async_session)
) -> Topic:
    topic = await get_obj_or_404(session=session, obj=Topic, id=id)

    return topic


async def valid_collection_id(
    *, id: int, session: AsyncSession = Depends(get_async_session)
) -> Collection:
    collection = await get_obj_or_404(session=session, obj=Collection, id=id)

    return collection
