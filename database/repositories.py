from shared.dto import ItemCreateDTO
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
