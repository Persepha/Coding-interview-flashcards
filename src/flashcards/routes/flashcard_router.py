from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from database import get_async_session
from flashcards.dependencies import valid_flashcard_id
from flashcards.models.flashcard import Flashcard
from flashcards.schemas.flashcard_schemas import (FlashcardCreateModel,
                                                  FlashcardModel,
                                                  FlashcardUpdateModel)
from flashcards.service import (flashcard_create, flashcard_delete,
                                flashcard_list, flashcard_update)

router = APIRouter()


@router.get("/", response_model=List[FlashcardModel])
async def flashcard_list_api(session: AsyncSession = Depends(get_async_session)):
    flashcards = await flashcard_list(session=session)

    return flashcards


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def flashcard_create_api(
    flashcard: FlashcardCreateModel, session: AsyncSession = Depends(get_async_session)
):
    new_flashcard = await flashcard_create(session=session, flashcard_dto=flashcard)

    return new_flashcard


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=FlashcardModel)
async def flashcard_detail_api(flashcard: Flashcard = Depends(valid_flashcard_id)):
    return flashcard


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def flashcard_detail_api(
    flashcard: Flashcard = Depends(valid_flashcard_id),
    session: AsyncSession = Depends(get_async_session),
):
    deleted_flashcard = await flashcard_delete(session=session, flashcard=flashcard)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}/update", status_code=status.HTTP_202_ACCEPTED, response_model=FlashcardModel
)
async def flashcard_update_api(
    flashcard_update_dto: FlashcardUpdateModel,
    flashcard: Flashcard = Depends(valid_flashcard_id),
    session: AsyncSession = Depends(get_async_session),
):
    updated_flashcard = await flashcard_update(
        session=session, flashcard=flashcard, flashcard_update_dto=flashcard_update_dto
    )

    return updated_flashcard
