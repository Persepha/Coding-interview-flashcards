from typing import Iterable, List

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from flashcards.models.flashcard import Flashcard
from flashcards.models.tag import Tag
from flashcards.schemas.flashcard_schemas import (FlashcardCreateModel,
                                                  FlashcardUpdateModel,
                                                  FlashcardWithTagsCreateModel)
from flashcards.schemas.tag_schemas import TagCreateModel, TagUpdateModel


async def flashcard_list(*, session: AsyncSession) -> Iterable[Flashcard]:
    query = select(Flashcard).order_by(Flashcard.id)
    flashcards = await session.execute(query)

    return flashcards.scalars().all()


async def flashcard_with_tags_list(*, session: AsyncSession):
    query = select(Flashcard).options(joinedload(Flashcard.tags))
    flashcards = await session.execute(query)

    return flashcards.scalars().unique().all()


async def get_tag_by_id(*, id: int, session: AsyncSession) -> Tag:
    query = select(Tag).where(Tag.id == id)
    tag = await session.execute(query)

    return tag.scalar()


async def get_tags_by_ids(
    *, session: AsyncSession, tags_ids: List[int]
) -> Iterable[Tag]:
    tags: List[Tag] = []

    for tag_id in tags_ids:
        tag = await get_tag_by_id(id=tag_id, session=session)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with the id {tag_id} is not available",
            )

        tags.append(tag)

    return tags


async def flashcard_create(
    *, session: AsyncSession, flashcard_dto: FlashcardWithTagsCreateModel
) -> Flashcard:
    data = flashcard_dto.dict()
    tags_ids = data.pop("tags_ids")

    new_flashcard = Flashcard(**data)

    if tags_ids is not None:
        tags = await get_tags_by_ids(session=session, tags_ids=tags_ids)
        new_flashcard.tags = tags

    session.add(new_flashcard)
    await session.commit()

    return new_flashcard


async def get_flashcard_by_id(*, id: int, session: AsyncSession) -> Flashcard:
    query = (
        select(Flashcard).options(joinedload(Flashcard.tags)).where(Flashcard.id == id)
    )
    flashcard = await session.execute(query)

    return flashcard.scalar()


async def flashcard_delete(*, session: AsyncSession, flashcard: Flashcard):
    await session.delete(flashcard)
    await session.commit()

    return flashcard


async def flashcard_update(
    *,
    session: AsyncSession,
    flashcard: Flashcard,
    flashcard_update_dto: FlashcardUpdateModel,
):
    data = flashcard_update_dto.dict(exclude_unset=True)
    tags_ids = data.pop("tags_ids", None)

    for field in data:
        if getattr(flashcard, field) != data[field]:
            setattr(flashcard, field, data[field])

    if tags_ids is not None:
        tags = await get_tags_by_ids(session=session, tags_ids=tags_ids)
        flashcard.tags = tags

    await session.commit()

    return flashcard


async def tag_list(*, session: AsyncSession) -> Iterable[Tag]:
    query = select(Tag).order_by(Tag.id)
    tags = await session.execute(query)

    return tags.scalars().all()


async def tag_create(*, session: AsyncSession, tag_dto: TagCreateModel) -> Tag:
    data = tag_dto.dict()
    new_tag = Tag(**data)

    session.add(new_tag)
    await session.commit()

    return new_tag


async def tag_delete(*, session: AsyncSession, tag: Tag):
    await session.delete(tag)
    await session.commit()

    return tag


async def tag_update(
    *, session: AsyncSession, tag: Tag, tag_update_dto: TagUpdateModel
):
    data = tag_update_dto.dict(exclude_unset=True)

    for field in data:
        if getattr(tag, field) != data[field]:
            setattr(tag, field, data[field])

    await session.commit()

    return tag
