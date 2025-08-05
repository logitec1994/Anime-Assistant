from models.media import MediaCategory, MediaBase
from database.db import Database
from repositories.media_repository import MediaRepository
from services.media_service import MediaService

def main():
    # Initialize
    db = Database()
    repository = MediaRepository(db)
    service = MediaService(repository)

    try:
        media_data = MediaBase(title="Attack on Titan3", category=MediaCategory.ANIME)
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        media_data = MediaBase(title="Attack on Titan", category=MediaCategory.MANGA)
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        media_data = MediaBase(title="Attack on Titan", category=MediaCategory.ANIME)
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    

    # Получение всех элементов
    items = service.get_all_media()
    print("\nВсе элементы в базе:")
    for item in items:
        print(f"ID={item.id}, Title={item.title}, Category={item.category.name}")


if __name__ == "__main__":
    main()
