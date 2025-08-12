from shared.dto import ItemCreateDTO, ItemUpdateDTO
from database.models import Item
from sqlalchemy.ext.asyncio import AsyncSession


class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def add_item(self, item: ItemCreateDTO) -> Item:
        new_item = Item(
            title=item.title,
            status=item.status,
            category=item.category
        )

        await self.db_session.add(new_item)
        return new_item
    
    async def get_all_items(self) -> list[Item]:
        return await self.db_session.query(Item).all()
    
    async def update_item_status(self, updated_item: ItemUpdateDTO) -> Item | None:
        item = await self.get_item_by_id(updated_item.id)
        if not item:
            return None
        item.status = updated_item.status
        await self.db_session.commit()
        await self.db_session.refresh(item)
        return item
    
    async def get_item_by_id(self, item_id: int) -> Item | None:
        return await self.db_session.query(Item).filter(Item.id == item_id).first()
