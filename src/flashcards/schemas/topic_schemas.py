from typing import List

from pydantic import BaseModel, Field

from flashcards.schemas.collection_schemas import (CollectionModel,
                                                   CollectionPreviewModel)


class TopicModel(BaseModel):
    id: int
    name: str
    collections: List[CollectionModel]

    class Config:
        orm_mode = True


class TopicPreviewModel(BaseModel):
    id: int
    name: str
    collections: List[CollectionPreviewModel]

    class Config:
        orm_mode = True


class TopicCreateModel(BaseModel):
    name: str = Field(max_length=100)


class TopicUpdateModel(BaseModel):
    name: str | None = None
