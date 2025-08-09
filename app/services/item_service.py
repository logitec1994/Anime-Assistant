from sqlalchemy.orm import Session
from database.repositories import ItemRepository
from shared.dto import ItemCreateDTO

class ItemService:
    def __init__(self, db_session: Session):
        self.repository = ItemRepository(db_session)
    
    def add_item(self, item: ItemCreateDTO) -> ItemCreateDTO:
        new_item = self.repository.add_item(item)
        self.repository.db_session.commit()
        self.repository.db_session.refresh(new_item)
        returned_item = ItemCreateDTO(
            # Need to use new_item instead of getattr
            id=getattr(new_item, "id"), # To avoid type incompatibility warning
            title=getattr(new_item, "title"), # To avoid type incompatibility warning
            status=getattr(new_item, "status"), # To avoid type incompatibility warning
            category=getattr(new_item, "category") # To avoid type incompatibility warning
        )

        return returned_item
