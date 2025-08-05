from models.media import MediaCategory, MediaBase, MediaStatus
from database.db import Database
from repositories.media_repository import MediaRepository
from services.media_service import MediaService

def main():
    # Initialize
    db = Database()
    repository = MediaRepository(db)
    service = MediaService(repository)

    # db.recreate_table()

    # Добавление "Naruto" как ANIME без указания статуса (должен быть WANT_TO_WATCH)
    try:
        media_data = MediaBase(
            title="Naruto",
            category=MediaCategory.ANIME
        )
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
        print(f"ID: {new_item.id}")
        print(f"Title: {new_item.title}")
        print(f"Category: {new_item.category}")
        print(f"Status: {new_item.status.name if new_item.status else 'None'}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Добавление "Naruto" как MANGA с явным статусом WATCHED
    try:
        media_data = MediaBase(
            title="Naruto",
            category=MediaCategory.MANGA,
            status=MediaStatus.WATCHED
        )
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
        print(f"ID: {new_item.id}")
        print(f"Title: {new_item.title}")
        print(f"Category: {new_item.category}")
        print(f"Status: {new_item.status.name if new_item.status else 'None'}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Попытка добавить дубликат "Naruto" как ANIME
    try:
        media_data = MediaBase(
            title="Naruto",
            category=MediaCategory.ANIME,
            status=MediaStatus.WATCHED
        )
        new_item = service.add_media(media_data)
        print(f"Added: {new_item}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Получение всех элементов
    items = service.get_all_media()
    print("\nВсе элементы в базе:")
    for item in items:
        status_str = item.status.name if item.status else "None"
        print(f"ID={item.id}, Title={item.title}, Category={item.category.name}, Status={status_str}")


if __name__ == "__main__":
    main()
