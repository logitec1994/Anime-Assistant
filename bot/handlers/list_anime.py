from aiogram import Router, types, F
from aiogram.filters import Command
from loguru import logger
from db.database import Database
from db.models import User, Anime, UserAnime, AnimeStatus
from bot.keyboards import (
    get_list_category_keyboard,
    get_pagination_keyboard,
    get_list_anime_keyboard_with_actions,
    get_detail_actions_keyboard,
    get_confirm_delete_keyboard
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import math

from aiogram.fsm.context import FSMContext
from bot.states import EditAnime

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
    
    list_text = "\n".join([f"{entry.anime.title}" for entry in anime_entries])

    footer = f"\n\nTotal anime: {total_count}"

    text = f"{header}{list_text}{footer}"

    list_actions_keyboard = get_list_anime_keyboard_with_actions(anime_entries)
    pagination_keyboard = get_pagination_keyboard(current_page, total_pages, category_str)

    combined_keyboard_builder = InlineKeyboardBuilder()
    combined_keyboard_builder.attach(InlineKeyboardBuilder.from_markup(list_actions_keyboard))
    combined_keyboard_builder.attach(InlineKeyboardBuilder.from_markup(pagination_keyboard))

    final_keyboard = combined_keyboard_builder.as_markup()

    if edit_message:
        await message.edit_text(text, reply_markup=final_keyboard)
    else:
        await message.answer(text, reply_markup=final_keyboard)

@router.callback_query(F.data.startswith("show_actions:"))
async def show_anime_details_and_actions(callback: types.CallbackQuery, db_session: Database):
    await callback.answer()

    user_anime_id = int(callback.data.split(":")[1])

    user_anime_entry = db_session.fetch_user_anime_entry(user_anime_id)
    if not user_anime_entry or user_anime_entry.user.telegram_id != callback.from_user.id:
        await callback.message.edit_text("Anime not found or you don't have access to it.")
        logger.error(f"User tried to access non-existing anime entry with ID {user_anime_id}")
        return
    
    anime_title = user_anime_entry.anime.title
    status_text = {
        AnimeStatus.TO_WATCH: "📺 Буду смотреть",
        AnimeStatus.WATCHING: "👀 Смотрю сейчас",
        AnimeStatus.WATCHED: "✅ Просмотрено",
        AnimeStatus.REWATCH: "🔄 Пересмотреть"
    }.get(user_anime_entry.status, "❓ Неизвестный статус")

    details_text = f"**Anime details:**\n\n" \
                   f"Title: {anime_title}\n" \
                   f"Status: {status_text}\n"
    
    if user_anime_entry.status == AnimeStatus.WATCHING:
        details_text += f"Current episode: {user_anime_entry.current_episode}\n"
        if user_anime_entry.watched_time_in_sec > 0:
            minutes = user_anime_entry.watched_time_in_sec // 60
            seconds = user_anime_entry.watched_time_in_sec % 60
            details_text += f"Watched time: {minutes:02d}:{seconds:02d}\n"

    if user_anime_entry.anime.total_episodes:
        details_text += f"Всего серий: `{user_anime_entry.anime.total_episodes}`\n"
    if user_anime_entry.anime.mal_id:
        details_text += f"MAL ID: `{user_anime_entry.anime.mal_id}`\n"

    details_text += f"Добавлено: `{user_anime_entry.added_at.strftime('%Y-%m-%d %H:%M')}`"
    
    await callback.message.edit_text(
        details_text,
        reply_markup=get_detail_actions_keyboard(user_anime_id),
        parse_mode="Markdown"
    )
    logger.info(f"User {callback.from_user.id} viewed details for anime entry ID {user_anime_id}")

@router.callback_query(F.data.startswith("back_to_list_from_detail"))
async def back_to_list(callback: types.CallbackQuery, db_session: Database):
    await callback.answer()

    user_id = callback.from_user.id
    db_user = db_session.get_user_by_telegram_id(user_id)

    if not db_user:
        await callback.message.answer("You need to start the bot first with /start command.")
        logger.error(f"User {user_id} not found in database.")
        return
    
    user_anime_entries, total_count = db_session.get_user_anime_list(
        user_id=db_user.id,
        status=None,
        offset=0,
        limit=ITEMS_PER_PAGE
    )

    total_pages = math.ceil(total_count / ITEMS_PER_PAGE) if total_count > 0 else 1
    current_page = 0
    category_str = "all"

    await send_anime_list_message(
        callback.message,
        user_anime_entries,
        total_count,
        current_page,
        total_pages,
        category_str,
        edit_message=True
    )
    logger.info(f"User {user_id} returned to anime list from details view.")

@router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete_anime_entry(callback: types.CallbackQuery, db_session: Database):
    await callback.answer()
    user_anime_id = int(callback.data.split(":")[1])

    user_anime_entry = db_session.fetch_user_anime_entry(user_anime_id)
    if not user_anime_entry or user_anime_entry.user.telegram_id != callback.from_user.id:
        await callback.message.edit_text("Извините, не удалось найти это аниме или у вас нет к нему доступа.")
        logger.warning(f"Пользователь {callback.from_user.id} пытался подтвердить удаление чужого или несуществующего user_anime_id: {user_anime_id}")
        return
    
    await callback.message.edit_text(
        "Вы уверены, что хотите удалить это аниме из вашего списка?",
        reply_markup=get_confirm_delete_keyboard(user_anime_id),
        parse_mode="Markdown"
    )
    logger.info(f"User {callback.from_user.id} confirmed delete action for anime entry ID {user_anime_id}")

@router.callback_query(F.data.startswith("delete_confirmed:"))
async def delete_anime_entry(callback: types.CallbackQuery, db_session: Database):
    await callback.answer("Deleting entry...")

    user_anime_id = int(callback.data.split(":")[1])

    user_anime_entry = db_session.fetch_user_anime_entry(user_anime_id)
    if not user_anime_entry or user_anime_entry.user.telegram_id != callback.from_user.id:
        await callback.message.edit_text("Anime entry not found or you don't have access to it.")
        logger.error(f"User {callback.from_user.id} tried to delete non-existing or unauthorized anime entry ID {user_anime_id}")
        return
    
    if db_session.delete_user_anime_entry(user_anime_id):
        await callback.message.edit_text("Anime entry successfully deleted.")
        logger.info(f"User {callback.from_user.id} deleted anime entry ID {user_anime_id}")
    else:
        await callback.message.edit_text("Failed to delete anime entry. Please try again later.")
        logger.error(f"Failed to delete anime entry ID {user_anime_id} for user {callback.from_user.id}")

    # await back_to_list(callback, db_session) # Можно раскомментировать для автоматического возврата к списку

@router.callback_query(F.data.startswith("delete_cancelled:"))
async def cancel_delete_anime_entry(callback: types.CallbackQuery, db_session: Database):
    await callback.answer("Delete action cancelled.")

    user_anime_id = int(callback.data.split(":")[1])

    await show_anime_details_and_actions(callback, db_session)
    logger.info(f"User {callback.from_user.id} cancelled delete action for anime entry ID {user_anime_id}")

@router.callback_query(F.data.startswith("edit_entry:"))
async def start_edit_anime_entry(callback: types.CallbackQuery, state: FSMContext, db_session: Database):
    await callback.answer("Начинаем редактирование...")
    user_anime_id = int(callback.data.split(":")[1])

    user_anime_entry = db_session.fetch_user_anime_entry(user_anime_id)
    if not user_anime_entry or user_anime_entry.user.telegram_id != callback.from_user.id:
        await callback.message.edit_text("Извините, не удалось найти это аниме или у вас нет к нему доступа.")
        logger.warning(f"Пользователь {callback.from_user.id} пытался редактировать чужое или несуществующее user_anime_id: {user_anime_id}")
        return
    
    await state.update_data(user_anime_id=user_anime_id, anime_title=user_anime_entry.anime.title)
    await callback.message.edit_text(
        f"Вы начали редактирование аниме: {user_anime_entry.anime.title}. "
        "Пожалуйста, выберите, что вы хотите изменить:",
        reply_markup=None # Soon
    )
    logger.info(f"User {callback.from_user.id} started editing anime entry ID {user_anime_id}")
