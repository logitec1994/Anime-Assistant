from app.services.item_service import ItemService
from database.session import SessionLocal
from shared.dto import ItemCreateDTO

if __name__ == "__main__":
    title = "Naruto"
    db_session = SessionLocal()
    service = ItemService(db_session)
    anime_item = ItemCreateDTO(title=title)
    item = service.add_item(anime_item)
