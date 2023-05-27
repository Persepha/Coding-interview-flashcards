from typing import Iterable, List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.services import CRUDBase
from flashcards.models.tag import Tag
from flashcards.schemas.tag_schemas import TagCreateModel, TagUpdateModel


class CRUDTag(CRUDBase[Tag, TagCreateModel, TagUpdateModel]):
    async def get_tags_by_ids(
        self, *, session: AsyncSession, tags_ids: List[int]
    ) -> Iterable[Tag]:
        tags: List[Tag] = []

        for tag_id in tags_ids:
            tag = await self.get_by_id(id=tag_id, session=session)

            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with the id {tag_id} is not available",
                )

            tags.append(tag)

        return tags


tag_crud = CRUDTag(Tag)
