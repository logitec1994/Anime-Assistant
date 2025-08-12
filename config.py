from pathlib import Path

DB_NAME = "anime_list.db"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / DB_NAME

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
