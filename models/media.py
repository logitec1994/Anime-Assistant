from enum import Enum, auto
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MediaCategory(Enum):
    ANIME = auto()
    MANGA = auto()


class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(SQLAlchemyEnum(MediaCategory, native_enum=True), nullable=False)

    __table_args__ = (UniqueConstraint('title', 'category', name='unique_title_category'),)

    def __str__(self):
        return f"MeidaItem(id={self.id}, title='{self.title}', category={self.category.name})"

class MediaBase(BaseModel):
    title: str
    category: MediaCategory

    class Config:
        arbitrary_types_allowed = True
