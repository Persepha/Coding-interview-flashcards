from fastapi import APIRouter

from auth.router import router as auth_router
from flashcards.routes.collection_router import router as collection_router
from flashcards.routes.flashcard_router import router as flashcard_router
from flashcards.routes.tag_router import router as tag_router
from flashcards.routes.topic_router import router as topic_router

api_router = APIRouter()

api_router.include_router(flashcard_router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(tag_router, prefix="/tags", tags=["tags"])
api_router.include_router(auth_router)
api_router.include_router(topic_router, prefix="/topics", tags=["topics"])
api_router.include_router(
    collection_router, prefix="/collections", tags=["collections"]
)
