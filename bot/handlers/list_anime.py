from aiogram import Router, types, F
from aiogram.filters import Command
from loguru import logger
from db.database import Database
from db.models import User, Anime, UserAnime, AnimeStatus # Anime нужен для entry.anime.title
from bot.keyboards import (
    get_list_category_keyboard,
    get_pagination_keyboard,
    get_anime_actions_keyboard # Пока не используется, но понадобится для деталей/редактирования
)
import math

router = Router()

ITEMS_PER_PAGE = 5

@router.message(Command("list", "mylist"))
async def cmd_list_anime(message: types.Message):
    logger.info(f"User {message.from_user.id} requested their anime list.")
    await message.answer("Please select a category to view your anime list.", reply_markup=get_list_category_keyboard())

@router.callback_query(F.data.startswith("list_cat:"))
async def process_list_category(callback: types.CallbackQuery, db_session: Database):
    await callback.answer()

    category_str = callback.data.split(":")[1]
    status_filter = None
    if category_str != "all":
        status_filter = AnimeStatus(category_str)

    user_id = callback.from_user.id
    db_user = db_session.get_user_by_telegram_id(user_id)
    if not db_user:
        await callback.message.answer("You need to start the bot first with /start command.")
        logger.error(f"User {user_id} not found in database.")
        return
    
    user_anime_entries, total_count = db_session.get_user_anime_list(
        user_id=db_user.id,
        status=status_filter,
        offset=0,
        limit=ITEMS_PER_PAGE
    )

    total_pages = math.ceil(total_count / ITEMS_PER_PAGE) if total_count > 0 else 1
    current_page = 0

    await send_anime_list_message(
        callback.message,
        user_anime_entries,
        total_count,
        current_page,
        total_pages,
        category_str
    )

@router.callback_query(F.data.startswith("list_page:"))
async def process_list_pagination(callback: types.CallbackQuery, db_session: Database):
    await callback.answer()

    _, category_str, page_str = callback.data.split(":")
    current_page = int(page_str)

    status_filter = None
    if category_str != "all":
        status_filter = AnimeStatus(category_str)

    user_id = callback.from_user.id
    db_user = db_session.get_user_by_telegram_id(user_id)

    if not db_user:
        await callback.message.answer("You need to start the bot first with /start command.")
        logger.error(f"User {user_id} not found in database.")
        return
    
    offset = current_page * ITEMS_PER_PAGE
    user_anime_entries, total_count = db_session.get_user_anime_list(
        user_id=db_user.id,
        status=status_filter,
        offset=offset,
        limit=ITEMS_PER_PAGE
    )

    total_pages = math.ceil(total_count / ITEMS_PER_PAGE) if total_count > 0 else 1

    await send_anime_list_message(
        callback.message,
        user_anime_entries,
        total_count,
        current_page,
        total_pages,
        category_str,
        edit_message=True
    )

async def send_anime_list_message(
    message: types.Message,
    anime_entries: list[UserAnime],
    total_count: int,
    current_page: int,
    total_pages: int,
    category_str: str,
    edit_message: bool = False
):
    if not anime_entries:
        text = "Your anime list is empty. Please add some anime first!"
        if edit_message:
            await message.edit_text(text)
        else:
            await message.answer(text)
        return
    
    header = ""

    if category_str == "all":
        header = f"Your full anime list:\n"
    else:
        status_name = {
            AnimeStatus.TO_WATCH.value: "To Watch",
            AnimeStatus.WATCHING.value: "Watching",
            AnimeStatus.WATCHED.value: "Watched",
            AnimeStatus.REWATCH.value: "Rewatch",
        }.get(category_str, "Unknown Category")
        header = f"Your anime list for category {status_name}: \n"

    list_items = []
    for i, entry in enumerate(anime_entries):
        item_number = current_page * ITEMS_PER_PAGE + i + 1
        title = entry.anime.title
        status_emoji = {
            AnimeStatus.TO_WATCH: "📺",
            AnimeStatus.WATCHING: "👀",
            AnimeStatus.WATCHED: "✅",
            AnimeStatus.REWATCH: "🔄"
        }.get(entry.status, "❓")

        episode_info = ""
        if entry.status == AnimeStatus.WATCHING:
            episode_info = f" (Episode {entry.current_episode})"
            if entry.watched_time_in_sec > 0:
                episode_info += f" - {entry.watched_time_in_sec // 60} min wathced"
        list_items.append(f"{item_number}. {status_emoji} {title}{episode_info}")

    list_text = "\n".join(list_items)
    footer = f"\n\nTotal anime: {total_count}"

    text = f"{header}{list_text}{footer}"

    pagination_keyboard = get_pagination_keyboard(current_page, total_pages, category_str)

    if edit_message:
        await message.edit_text(text, reply_markup=pagination_keyboard)
    else:
        await message.answer(text, reply_markup=pagination_keyboard)
