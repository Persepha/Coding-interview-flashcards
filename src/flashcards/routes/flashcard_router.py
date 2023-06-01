from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from auth.auth_config import current_superuser
from auth.models import User
from database import get_async_session
from flashcards.dependencies import valid_flashcard_id
from flashcards.models.flashcard import Flashcard
from flashcards.schemas.flashcard_schemas import (FlashcardUpdateModel,
                                                  FlashcardWithTagsCreateModel,
                                                  FlashcardWithTagsModel)
from flashcards.services.flashcard import flashcard_crud

router = APIRouter()


@router.get("/", response_model=List[FlashcardWithTagsModel])
async def flashcard_list_api(session: AsyncSession = Depends(get_async_session)):
    flashcards = await flashcard_crud.get_list_with_tags(session=session)

    return flashcards


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def flashcard_create_api(
    create_dto: FlashcardWithTagsCreateModel,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    new_flashcard = await flashcard_crud.create_with_tags(
        session=session, create_dto=create_dto, creator_id=user.id
    )

    return new_flashcard


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=FlashcardWithTagsModel,
)
async def flashcard_detail_api(
    flashcard: Flashcard = Depends(valid_flashcard_id),
    session: AsyncSession = Depends(get_async_session),
):
    flashcard_with_tags = await flashcard_crud.get_flashcard_with_tags_by_id(
        id=flashcard.id, session=session
    )
    return flashcard_with_tags


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def flashcard_delete_api(
    flashcard: Flashcard = Depends(valid_flashcard_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    deleted_flashcard = await flashcard_crud.delete(session=session, obj=flashcard)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/update",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=FlashcardWithTagsModel,
)
async def flashcard_update_api(
    flashcard_update_dto: FlashcardUpdateModel,
    flashcard: Flashcard = Depends(valid_flashcard_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    flashcard_with_tags = await flashcard_crud.get_flashcard_with_tags_by_id(
        id=flashcard.id, session=session
    )

    updated_flashcard = await flashcard_crud.update(
        session=session,
        flashcard=flashcard_with_tags,
        flashcard_update_dto=flashcard_update_dto,
    )

    return updated_flashcard
