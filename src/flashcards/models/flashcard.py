from sqlalchemy import (Column, ForeignKey, Identity, Integer, String, Table,
                        Text)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from auth.models import User
from database import Base
from flashcards.models.topic import Topic


class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    question = Column(String)
    answer = Column(Text)

    tags = relationship("Tag", secondary="flashcard_tags", back_populates="flashcards")

    creator_id = Column(Integer, ForeignKey(User.id))
    creator = relationship("User", back_populates="flashcards")

    collections = relationship(
        "Collection", secondary="collection_flashcards", back_populates="flashcards"
    )


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    name = Column(String)

    creator_id = Column(Integer, ForeignKey(User.id))
    creator = relationship("User", back_populates="collections")

    topic_id = Column(Integer, ForeignKey(Topic.id))
    topic = relationship("Topic", back_populates="collections")

    flashcards = relationship(
        "Flashcard", secondary="collection_flashcards", back_populates="collections"
    )


flashcard_tags = Table(
    "flashcard_tags",
    Base.metadata,
    Column("flashcard_id", ForeignKey("flashcard.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)

collection_flashcards = Table(
    "collection_flashcards",
    Base.metadata,
    Column("collection_id", ForeignKey("collection.id"), primary_key=True),
    Column("flashcard_id", ForeignKey("flashcard.id"), primary_key=True),
)
