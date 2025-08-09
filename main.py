from app.services.item_service import ItemService
from database.session import SessionLocal
from shared.dto import ItemCreateDTO, ItemUpdateDTO
from shared.enums import ItemStatus, ItemCategory

if __name__ == "__main__":
    # title = "Naruto"
    with SessionLocal() as db_session:
        service = ItemService(db_session)
        item_list = service.get_items()
        print(item_list)

        print("\nBefore update")

        update_item = ItemUpdateDTO(id=2, status=ItemStatus.WATCHED)
        result = service.update_status(update_item)
        print(result)

        print("After update\n")

        item_list = service.get_items()
        print(item_list)

    print(item_list)
