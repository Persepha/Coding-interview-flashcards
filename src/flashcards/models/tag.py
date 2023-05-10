from sqlalchemy import Column, Identity, Integer, String, Text

from database import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    name = Column(String(100))
