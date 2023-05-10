from sqlalchemy import Column, Identity, Integer, String, Text

from database import Base


class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    question = Column(String)
    answer = Column(Text)
