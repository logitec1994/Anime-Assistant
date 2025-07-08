from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db.base import Base

class UserMedia(Base):
    __tablename__ = "user_media"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(foreign_key="users.id")
    title: Mapped[str]
    type: Mapped[str]
    total: Mapped[int]
    progress: Mapped[int]
    rating: Mapped[int | None]
