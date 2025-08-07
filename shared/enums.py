from enum import Enum, auto

class ItemStatus(Enum):
    WANT_TO_WATCH = auto()
    WATCHED = auto()

class ItemCategory(Enum):
    ANIME = auto()
    MANGA = auto()
    MOVIE = auto()
    SERIES = auto()
