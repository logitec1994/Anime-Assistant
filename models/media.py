from enum import Enum, auto
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.orm import declarative_base
from typing import Optional

Base = declarative_base()

class MediaCategory(Enum):
    ANIME = auto()
    MANGA = auto()

class MediaStatus(Enum):
    WATCHED = auto()
    WANT_TO_WATCH = auto()

class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(SQLAlchemyEnum(MediaCategory, native_enum=True), nullable=False)
    status = Column(SQLAlchemyEnum(MediaStatus, native_enum=False), nullable=True)

    __table_args__ = (UniqueConstraint('title', 'category', name='unique_title_category'),)

    def __str__(self):
        status_str = self.status.name if self.status else "None"
        return f"MeidaItem(id={self.id}, title='{self.title}', category={self.category.name}, status={status_str})"

class MediaBase(BaseModel):
    title: str
    category: MediaCategory
    status: Optional[MediaStatus] = MediaStatus.WANT_TO_WATCH

    class Config:
        arbitrary_types_allowed = True
