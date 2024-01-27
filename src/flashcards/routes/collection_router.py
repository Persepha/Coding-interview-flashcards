import json
from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_superuser
from auth.models import User
from database import get_async_session
from flashcards.dependencies import valid_collection_id
from flashcards.models.flashcard import Collection
from flashcards.schemas.collection_schemas import (CollectionCreateModel,
                                                   CollectionModel,
                                                   CollectionUpdateModel)
from flashcards.services.collection import collection_crud

router = APIRouter()


@router.get("/", response_model=List[CollectionModel])
async def collection_list_api(session: AsyncSession = Depends(get_async_session)):
    collection_list = await collection_crud.get_list(session=session)

    return collection_list


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def collection_create_api(
    create_dto: CollectionCreateModel,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    new_collection = await collection_crud.create_with_flashcards(
        session=session, create_dto=create_dto, creator_id=user.id
    )

    return new_collection


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CollectionModel,
)
async def collection_detail_api(
    collection: Collection = Depends(valid_collection_id),
    session: AsyncSession = Depends(get_async_session),
):
    collection_with_flashcards = await collection_crud.get_collection_by_id(
        id=collection.id, session=session
    )
    print("-------------FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF--------")
    print(collection_with_flashcards)
    print("-------------FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF--------")
    return collection_with_flashcards


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def collection_delete_api(
    collection: Collection = Depends(valid_collection_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    deleted_collection = await collection_crud.delete(session=session, obj=collection)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/update",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CollectionModel,
)
async def flashcard_update_api(
    collection_update_dto: CollectionUpdateModel,
    collection: Collection = Depends(valid_collection_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    collection_with_flashcards = await collection_crud.get_collection_by_id(
        id=collection.id, session=session
    )

    updated_collection = await collection_crud.update(
        session=session,
        collection=collection_with_flashcards,
        collection_update_dto=collection_update_dto,
    )

    return updated_collection
