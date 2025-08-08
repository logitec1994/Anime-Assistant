from shared.dto import ItemCreateDTO
from database.init_db import init_db


if __name__ == "__main__":
    title = "Naruto"
    anime = ItemCreateDTO(title=title)

    init_db()
