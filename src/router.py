from fastapi import APIRouter

from flashcards.router import router as flashcards_router

api_router = APIRouter()

api_router.include_router(flashcards_router, prefix="/flashcards", tags=["flashcards"])
