from fastapi import APIRouter

from flashcards.routes.flashcard_router import router as flashcard_router
from flashcards.routes.tag_router import router as tag_router

api_router = APIRouter()

api_router.include_router(flashcard_router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(tag_router, prefix="/tags", tags=["tags"])
