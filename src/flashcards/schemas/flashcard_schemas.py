from pydantic import BaseModel
from pydantic.fields import List

from auth.schemas import UserRead
from flashcards.schemas.tag_schemas import TagCreateModel, TagModel


class FlashcardModel(BaseModel):
    id: int
    question: str
    answer: str
    creator_id: int
    creator: UserRead

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
