from pydantic import BaseModel
from pydantic.fields import List

from flashcards.schemas.tag_schemas import TagCreateModel, TagModel


class FlashcardModel(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True


class FlashcardCreateModel(BaseModel):
    question: str
    answer: str


class FlashcardUpdateModel(BaseModel):
    question: str | None = None
    answer: str | None = None
    tags_ids: List[int] | None = None


class FlashcardWithTagsModel(FlashcardModel):
    tags: List[TagModel]


class FlashcardWithTagsCreateModel(FlashcardCreateModel):
    tags_ids: List[int] | None = None
