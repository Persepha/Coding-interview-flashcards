from typing import List

from pydantic import BaseModel

from auth.schemas import UserRead
from flashcards.schemas.flashcard_schemas import FlashcardModel


class TopicCollectionModel(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CollectionModel(BaseModel):
    id: int
    name: str
    creator: UserRead
    topic: TopicCollectionModel
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
