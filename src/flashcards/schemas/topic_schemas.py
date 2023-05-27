from pydantic import BaseModel, Field


class TopicModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TopicCreateModel(BaseModel):
    name: str = Field(max_length=100)


class TopicUpdateModel(BaseModel):
    name: str | None = None
