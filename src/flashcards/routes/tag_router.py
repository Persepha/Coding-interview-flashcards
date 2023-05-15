from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from auth.auth_config import current_superuser
from auth.models import User
from database import get_async_session
from flashcards.dependencies import valid_tag_id
from flashcards.models.tag import Tag
from flashcards.schemas.tag_schemas import (TagCreateModel, TagModel,
                                            TagUpdateModel)
from flashcards.service import tag_create, tag_delete, tag_list, tag_update

router = APIRouter()


@router.get("/", response_model=List[TagModel])
async def tag_list_api(session: AsyncSession = Depends(get_async_session)):
    tags = await tag_list(session=session)

    return tags


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def tag_create_api(
    tag: TagCreateModel,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    new_tag = await tag_create(session=session, tag_dto=tag)

    return new_tag


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=TagModel)
async def tag_detail_api(tag: Tag = Depends(valid_tag_id)):
    return tag


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def tag_delete_api(
    tag: Tag = Depends(valid_tag_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    deleted_tag = await tag_delete(session=session, tag=tag)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/update",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TagModel,
)
async def flashcard_update_api(
    tag_update_dto: TagUpdateModel,
    tag: Tag = Depends(valid_tag_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    updated_tag = await tag_update(
        session=session, tag=tag, tag_update_dto=tag_update_dto
    )

    return updated_tag
