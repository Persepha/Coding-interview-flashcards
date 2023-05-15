from sqlalchemy import (Column, ForeignKey, Identity, Integer, String, Table,
                        Text)
from sqlalchemy.orm import relationship

from auth.models import User
from database import Base


class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    question = Column(String)
    answer = Column(Text)

    tags = relationship("Tag", secondary="flashcard_tags", back_populates="flashcards")

    creator_id = Column(Integer, ForeignKey(User.id))
    creator = relationship("User", back_populates="flashcards")


flashcard_tags = Table(
    "flashcard_tags",
    Base.metadata,
    Column("flashcard_id", ForeignKey("flashcard.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
