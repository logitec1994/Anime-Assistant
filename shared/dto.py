from pydantic import BaseModel, Field
from shared.enums import ItemStatus, ItemCategory

class Item(BaseModel):
    id: int | None = None
    title: str
    status: ItemStatus = Field(default=ItemStatus.WANT_TO_WATCH)
    category: ItemCategory = Field(default=ItemCategory.ANIME)
