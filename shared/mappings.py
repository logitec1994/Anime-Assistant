from shared.enums import ItemCategory, ItemStatus

CATEGORY_MAPPINGS = {
    ItemCategory.ANIME: ("🎬 Аниме", "category_anime"),
    ItemCategory.MANGA: ("📖 Манга", "category_manga"),
    ItemCategory.MOVIE: ("🎥 Фильм", "category_movie"),
    ItemCategory.SERIES: ("📺 Сериал", "category_series")
}

STATUS_MAPPINGS = {
    ItemStatus.WANT_TO_WATCH: ("📋 Хочу посмотреть", "status_want_to_watch"),
    ItemStatus.WATCHED: ("✅ Посмотрел", "status_watched")
}

def get_category_mappings():
    return CATEGORY_MAPPINGS

def get_status_mappings():
    return STATUS_MAPPINGS