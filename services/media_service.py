from sqlalchemy.exc import IntegrityError
from models.media import MediaItem, MediaBase
from repositories.media_repository import MediaRepository

class MediaService:
    def __init__(self, repository: MediaRepository):
        self.repository = repository
    
    def add_media(self, media_data: MediaBase) -> MediaItem:
        item = MediaItem(title=media_data.title, category=media_data.category)
        try:
            self.repository.add_item(item)
            return item
        except IntegrityError:
            raise ValueError(f"Media item with title '{media_data.title}' and category '{media_data.category.name}' already exists.")
    
    def get_all_media(self) -> list[MediaItem]:
        return self.repository.get_all_items()
