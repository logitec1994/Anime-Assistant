from models.media import MediaStatus
from database.db import Database
from repositories.media_repository import MediaRepository
from services.media_service import MediaService

def main():
    # Initialize
    db = Database()
    repository = MediaRepository(db)
    service = MediaService(repository)

    # db.recreate_table()

    media = service.get_media_by_id(1)

    print(media)

    service.update_media_status(1, MediaStatus.WATCHED)

    items = service.get_all_media()
    for item in items:
        print(item.title, item.status)


if __name__ == "__main__":
    main()
