from app.services.media_service import MediaService
from database.repositories.media_repository import MediaRepository
from database.session import SessionLocal
from database.models.base import Base
from database.session import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Все таблицы созданы")

    with SessionLocal() as session:
        repo = MediaRepository(session)
        item = MediaService(repo)
        item.add_item("Naruto", "anime")
        # test = item.get_item_by_title("Naruto")

    # print(test)
