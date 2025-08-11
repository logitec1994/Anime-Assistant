from shared.enums import ItemCategory

CATEGORY_MAPPINGS = {
    ItemCategory.ANIME: ("🎬 Аниме", "category_anime"),
    ItemCategory.MANGA: ("📖 Манга", "category_manga"),
    ItemCategory.MOVIE: ("🎥 Фильм", "category_movie"),
    ItemCategory.SERIES: ("📺 Сериал", "category_series")
}

def get_category_mappings():
    return CATEGORY_MAPPINGS