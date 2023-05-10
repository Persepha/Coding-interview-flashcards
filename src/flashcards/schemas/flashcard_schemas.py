from pydantic import BaseModel


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
