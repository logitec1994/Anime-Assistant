from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
from database.session import Base
from shared.enums import ItemStatus, ItemCategory

class Item(Base):
    __tablename__ = "items"
    __table_args__ = (
        UniqueConstraint("title", "category", name="uix_title_category"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(Enum(ItemStatus), nullable=False)
    category = Column(Enum(ItemCategory), nullable=False)
