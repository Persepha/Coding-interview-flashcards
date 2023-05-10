from typing import Iterable

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.flashcard import Flashcard
from flashcards.models.tag import Tag
from flashcards.schemas.flashcard_schemas import (FlashcardCreateModel,
                                                  FlashcardUpdateModel)
from flashcards.schemas.tag_schemas import TagCreateModel


async def flashcard_list(*, session: AsyncSession) -> Iterable[Flashcard]:
    query = select(Flashcard).order_by(Flashcard.id)
    flashcards = await session.execute(query)

    return flashcards.scalars().all()


async def flashcard_create(
    *, session: AsyncSession, flashcard_dto: FlashcardCreateModel
) -> Flashcard:
    data = jsonable_encoder(flashcard_dto)
    new_flashcard = Flashcard(**data)

    session.add(new_flashcard)
    await session.commit()

    return new_flashcard


async def get_flashcard_by_id(*, id: int, session: AsyncSession) -> Flashcard:
    query = select(Flashcard).where(Flashcard.id == id)
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
    flashcard_update_dto: FlashcardUpdateModel
):
    data = flashcard_update_dto.dict(exclude_unset=True)

    for field in data:
        if getattr(flashcard, field) != data[field]:
            setattr(flashcard, field, data[field])

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
