from sqlalchemy.exc import IntegrityError
from models.media import MediaItem, MediaBase, MediaStatus
from repositories.media_repository import MediaRepository

class MediaService:
    def __init__(self, repository: MediaRepository):
        self.repository = repository
    
    def add_media(self, media_data: MediaBase) -> MediaItem:
        item = MediaItem(
            title=media_data.title,
            category=media_data.category,
            status=media_data.status
            )
        try:
            self.repository.add_item(item)
            return item
        except IntegrityError:
            raise ValueError(f"Media item with title '{media_data.title}' and category '{media_data.category.name}' already exists.")
    
    def get_all_media(self) -> list[MediaItem]:
        return self.repository.get_all_items()
    
    def get_media_by_id(self, item_id: int) -> MediaItem:
        return self.repository.get_item_by_id(item_id)
    
    def update_media_status(self, item_id: int, new_status: MediaStatus) -> MediaItem:
        updated_item = self.repository.update_status(item_id, new_status)
        if not updated_item:
            raise ValueError(f"Media item with ID {item_id} not found.")
        return updated_item