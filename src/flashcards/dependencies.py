from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select
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


async def valid_topic_name(
    *, name: str, session: AsyncSession = Depends(get_async_session)
) -> Topic:
    query = select(Topic).where(func.lower(Topic.name) == func.lower(name))
    result = await session.execute(query)

    topic = result.scalar()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with the name {name} is not available",
        )

    return topic
