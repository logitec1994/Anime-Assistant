from pydantic import BaseModel, Field
from shared.enums import ItemStatus, ItemCategory


class ItemCreateDTO(BaseModel):
    id: int | None = None
    title: str
    status: ItemStatus = Field(default=ItemStatus.WANT_TO_WATCH)
    category: ItemCategory = Field(default=ItemCategory.ANIME)

class ItemUpdateDTO(BaseModel):
    id: int
    status: ItemStatus
