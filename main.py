from enum import Enum, auto

class MediaCategory(Enum):
    ANIME = auto()
    MANGA = auto()


class MediaItem:
    def __init__(self, title, category: MediaCategory):
        self.title = title
        self.category = category

if __name__ == "__main__":
    media_category = MediaCategory.ANIME
    media_title = "Attack on Titan"
    media = MediaItem(media_title, media_category)
