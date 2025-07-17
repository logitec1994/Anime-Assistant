from typing import List
from models import MediaModel

class MediaRepository:
    def __init__(self) -> None:
        self.__media_list: List[MediaModel] = []
    
    def add_media(self, media: MediaModel) -> None:
        self.__media_list.append(media)
    
    def get_all_media(self) -> List[MediaModel]:
        return self.__media_list

    def get_media_by_title(self, title: str) -> MediaModel:
        for media in self.__media_list:
            if media.title == title:
                return media
    
    def exists(self, title: str) -> bool:
        return any(media.title == title for media in self.__media_list)
