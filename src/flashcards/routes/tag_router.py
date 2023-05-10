from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from flashcards.schemas.tag_schemas import TagCreateModel, TagModel
from flashcards.service import tag_create, tag_list

router = APIRouter()


@router.get("/", response_model=List[TagModel])
async def tag_list_api(session: AsyncSession = Depends(get_async_session)):
    tags = await tag_list(session=session)

    return tags


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def tag_create_api(
    tag: TagCreateModel, session: AsyncSession = Depends(get_async_session)
):
    new_tag = await tag_create(session=session, tag_dto=tag)

    return new_tag
