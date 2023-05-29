from typing import List

from pydantic import BaseModel

from auth.schemas import UserRead
from flashcards.schemas.flashcard_schemas import FlashcardModel
from flashcards.schemas.topic_schemas import TopicModel


class CollectionModel(BaseModel):
    id: int
    name: str
    creator: UserRead
    topic: TopicModel
    flashcards: List[FlashcardModel]

    class Config:
        orm_mode = True


class CollectionCreateModel(BaseModel):
    name: str
    topic_id: int
    flashcards_ids: List[int]


class CollectionUpdateModel(BaseModel):
    name: str | None = None
    topic_id: int | None = None
    flashcards_ids: List[int] | None = None
