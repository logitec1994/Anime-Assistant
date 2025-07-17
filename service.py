from dto import BaseDTO
from models import MediaModel
from repository import MediaRepository

class MediaService:
    def __init__(self, repo: MediaRepository) -> None:
        self.repo = repo
    
    def add_media(self, dto: BaseDTO) -> None:
        if self.repo.exists(dto.title):
            print(f"Media already exists with title: {dto.title}")
            return self.repo.get_media_by_title(dto.title)
        
        media = MediaModel(title=dto.title)
        self.repo.add_media(media)

        return media
    