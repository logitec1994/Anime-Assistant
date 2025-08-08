from enum import StrEnum

class ItemStatus(StrEnum):
    WANT_TO_WATCH = "want_to_watch"
    WATCHED = "watched"

class ItemCategory(StrEnum):
    ANIME = "anime"
    MANGA = "manga"
    MOVIE = "movie"
    SERIES = "series"
