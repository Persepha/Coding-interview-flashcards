from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_superuser
from auth.models import User
from database import get_async_session
from flashcards.dependencies import valid_topic_id, valid_topic_name
from flashcards.models.topic import Topic
from flashcards.schemas.topic_schemas import (TopicCreateModel, TopicModel,
                                              TopicPreviewModel,
                                              TopicUpdateModel)
from flashcards.services.topic import topic_crud

router = APIRouter()


@router.get("/", response_model=List[TopicModel])
async def topic_list_api(session: AsyncSession = Depends(get_async_session)):
    tags = await topic_crud.get_list_with_collections(session=session)

    return tags


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def topic_create_api(
    create_dto: TopicCreateModel,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    new_topic = await topic_crud.create(session=session, create_dto=create_dto)

    return new_topic


@router.get("/{name}", status_code=status.HTTP_200_OK, response_model=TopicPreviewModel)
async def topic_detail_api(
    topic: Topic = Depends(valid_topic_name),
    session: AsyncSession = Depends(get_async_session),
):
    topic_with_collections = await topic_crud.get_preview_by_id(
        session=session, id=topic.id
    )

    print(")))))))))))))))))))))))))))))))))))))))))")
    print(topic_with_collections)
    return topic_with_collections


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def topic_delete_api(
    topic: Topic = Depends(valid_topic_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    deleted_topic = await topic_crud.delete(session=session, obj=topic)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/update",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TopicModel,
)
async def topic_update_api(
    update_dto: TopicUpdateModel,
    topic: Topic = Depends(valid_topic_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    updated_topic = await topic_crud.update(
        session=session, obj=topic, update_dto=update_dto
    )

    return updated_topic
