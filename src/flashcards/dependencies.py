from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from flashcards.models import Flashcard
from flashcards.service import get_flashcard_by_id


async def valid_flashcard_id(
    *, id: int, session: AsyncSession = Depends(get_async_session)
) -> Flashcard:
    flashcard = await get_flashcard_by_id(id=id, session=session)

    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flashcard with the id {id} is not available",
        )

    return flashcard
