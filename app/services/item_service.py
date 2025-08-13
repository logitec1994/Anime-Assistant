from sqlalchemy.exc import IntegrityError
from database.repositories import ItemRepository
from shared.dto import ItemCreateDTO, ItemUpdateDTO

class ItemService:
    def __init__(self, db_session):
        self.repository = ItemRepository(db_session)
    
    def add_item(self, item: ItemCreateDTO) -> ItemCreateDTO | str:
        try:
            new_item = self.repository.add_item(item)
            self.repository.db_session.commit()
            self.repository.db_session.refresh(new_item)
            return ItemCreateDTO(
                id=new_item.id,
                title=new_item.title,
                status=new_item.status,
                category=new_item.category
            )
        except IntegrityError:
            self.repository.db_session.rollback()
            return f"Item already exists with title {item.title} and category {item.category}"
    
    def get_items(self) -> list[ItemCreateDTO]:
        items = self.repository.get_all_items()
        return [ItemCreateDTO(
            id=item.id,
            title=item.title,
            status=item.status,
            category=item.category
        ) for item in items]
    
    def update_status(self, item: ItemUpdateDTO) -> ItemCreateDTO | str:
        updated_item = self.repository.update_item_status(item)
        if not updated_item:
            return f"Item with id {item.id} not found"
        self.repository.db_session.commit()
        self.repository.db_session.refresh(updated_item)
        return ItemCreateDTO(
            id=updated_item.id,
            title=updated_item.title,
            status=updated_item.status,
            category=updated_item.category
        )
