from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_superuser
from auth.models import User
from database import get_async_session
from flashcards.schemas.collection_schemas import (CollectionCreateModel,
                                                   CollectionModel)
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
