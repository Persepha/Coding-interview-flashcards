from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    name = Column(String(100))

    collections = relationship("Collection", back_populates="topic")
