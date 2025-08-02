from app.models.media_item import MediaItemDTO
from database.repositories.media_repository import MediaRepository

class MediaService:
    def __init__(self, repo: MediaRepository) -> None:
        self.repo = repo

    def get_all_items(self) -> list[MediaItemDTO]:
        return self.repo.get_all()
    
    def add_item(self, title: str, category: str) -> MediaItemDTO:
        new_item = MediaItemDTO(
            title=title,
            category=category
        )
        return self.repo.save(new_item)
