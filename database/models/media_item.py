from sqlalchemy import Column, Integer, String, DateTime
from database.models.base import Base

class MediaItemORM(Base):
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
