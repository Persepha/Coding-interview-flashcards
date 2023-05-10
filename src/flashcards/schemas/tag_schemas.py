from pydantic import BaseModel, Field


class TagModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TagCreateModel(BaseModel):
    name: str = Field(max_length=100)
