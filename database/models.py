from sqlalchemy import Column, Integer, String, Enum
from database.session import Base
from shared.enums import ItemStatus, ItemCategory

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(Enum(ItemStatus), nullable=False)
    category = Column(Enum(ItemCategory), nullable=False)
