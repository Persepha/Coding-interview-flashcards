from typing import Iterable, List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from common.services import CRUDBase
from flashcards.models.flashcard import Flashcard
from flashcards.schemas.flashcard_schemas import (FlashcardCreateModel,
                                                  FlashcardUpdateModel,
                                                  FlashcardWithTagsCreateModel)
from flashcards.services.tag import tag_crud


class CRUDFlashcard(CRUDBase[Flashcard, FlashcardCreateModel, FlashcardUpdateModel]):
    async def get_list_with_tags(self, *, session: AsyncSession) -> Iterable[Flashcard]:
        query = select(Flashcard).options(
            joinedload(Flashcard.tags), joinedload(Flashcard.creator)
        )
        flashcards = await session.execute(query)

        return flashcards.scalars().unique().all()

    async def create_with_tags(
        self,
        *,
        session: AsyncSession,
        create_dto: FlashcardWithTagsCreateModel,
        creator_id: int,
    ) -> Flashcard:
        data = create_dto.dict()
        tags_ids = data.pop("tags_ids")

        new_flashcard = Flashcard(**data, creator_id=creator_id)

        if tags_ids is not None:
            tags = await tag_crud.get_tags_by_ids(session=session, tags_ids=tags_ids)
            new_flashcard.tags = tags

        session.add(new_flashcard)
        await session.commit()

        return new_flashcard

    async def get_flashcard_with_tags_by_id(
        self, *, id: int, session: AsyncSession
    ) -> Flashcard:
        query = (
            select(Flashcard)
            .options(joinedload(Flashcard.tags), joinedload(Flashcard.creator))
            .where(Flashcard.id == id)
        )
        flashcard = await session.execute(query)

        return flashcard.scalar()

    async def update(
        self,
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
            tags = await tag_crud.get_tags_by_ids(session=session, tags_ids=tags_ids)
            flashcard.tags = tags

        await session.commit()

        return flashcard

    async def get_flashcards_by_ids(
        self, *, session: AsyncSession, flashcards_ids: List[int]
    ) -> Iterable[Flashcard]:
        flashcards: List[Flashcard] = []

        for flashcard_id in flashcards_ids:
            flashcard = await self.get_by_id(id=flashcard_id, session=session)

            if not flashcard:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Flashcard with the id {flashcard_id} is not available",
                )

            flashcards.append(flashcard)

        return flashcards


flashcard_crud = CRUDFlashcard(Flashcard)
