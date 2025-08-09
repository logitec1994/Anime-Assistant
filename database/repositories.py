from shared.dto import ItemCreateDTO, ItemUpdateDTO
from database.models import Item
from sqlalchemy.orm import Session

class ItemRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def add_item(self, item: ItemCreateDTO) -> Item:
        new_item = Item(
            title=item.title,
            status=item.status,
            category=item.category
        )

        self.db_session.add(new_item)
        return new_item
    
    def get_all_items(self) -> list[Item]:
        return self.db_session.query(Item).all()
    
    def update_item_status(self, updated_item: ItemUpdateDTO) -> Item | None:
        item = self.get_item_by_id(updated_item.id)
        if not item:
            return None
        item.status = updated_item.status
        self.db_session.commit()
        self.db_session.refresh(item)
        return item
    
    def get_item_by_id(self, item_id: int) -> Item | None:
        return self.db_session.query(Item).filter(Item.id == item_id).first()
