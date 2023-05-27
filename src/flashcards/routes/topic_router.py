from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from flashcards.dependencies import valid_topic_id
from flashcards.models.topic import Topic
from flashcards.schemas.topic_schemas import (TopicCreateModel, TopicModel,
                                              TopicUpdateModel)
from flashcards.services.topic import topic_crud

router = APIRouter()


@router.get("/", response_model=List[TopicModel])
async def topic_list_api(session: AsyncSession = Depends(get_async_session)):
    tags = await topic_crud.get_list(session=session)

    return tags


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def topic_create_api(
    create_dto: TopicCreateModel,
    session: AsyncSession = Depends(get_async_session),
):
    new_topic = await topic_crud.create(session=session, create_dto=create_dto)

    return new_topic


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=TopicModel)
async def topic_detail_api(topic: Topic = Depends(valid_topic_id)):
    return topic


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def topic_delete_api(
    topic: Topic = Depends(valid_topic_id),
    session: AsyncSession = Depends(get_async_session),
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
):
    updated_topic = await topic_crud.update(
        session=session, obj=topic, update_dto=update_dto
    )

    return updated_topic
