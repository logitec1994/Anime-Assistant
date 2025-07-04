from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.models import AnimeStatus

def get_anime_status_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📺 Буду смотреть", callback_data=f"set_status:{AnimeStatus.TO_WATCH.value}"),
        InlineKeyboardButton(text="👀 Смотрю сейчас", callback_data=f"set_status:{AnimeStatus.WATCHING.value}")
    )
    builder.row(
        InlineKeyboardButton(text="✅ Просмотрено", callback_data=f"set_status:{AnimeStatus.WATCHED.value}"),
        InlineKeyboardButton(text="🔄 Пересмотреть", callback_data=f"set_status:{AnimeStatus.REWATCH.value}")
    )

    return builder.as_markup()

def get_list_category_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="All", callback_data="list_cat:all"),
        InlineKeyboardButton(text="To watch", callback_data=f"list_cat:{AnimeStatus.TO_WATCH.value}")
    )
    builder.row(
        InlineKeyboardButton(text="Watching", callback_data=f"list_cat:{AnimeStatus.WATCHING.value}"),
        InlineKeyboardButton(text="Watched", callback_data=f"list_cat:{AnimeStatus.WATCHED.value}")
    )
    builder.row(
        InlineKeyboardButton(text="Rewatch", callback_data=f"list_cat:{AnimeStatus.REWATCH.value}")
    )
    return builder.as_markup()

def get_pagination_keyboard(current_page: int, total_pages: int, category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if current_page > 0:
        builder.button(text="◀️ Previous", callback_data=f"list_page:{category}:{current_page - 1}")
    
    builder.button(text=f"Page {current_page + 1} / {total_pages}", callback_data="ignore_page_info")

    if current_page < total_pages - 1:
        builder.button(text="Next ▶️", callback_data=f"list_page:{category}:{current_page + 1}")

    return builder.as_markup()

def get_list_anime_keyboard_with_actions(anime_entries_on_page: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, entry in enumerate(anime_entries_on_page):
        builder.row(InlineKeyboardButton(text=f"{i + 1}. {entry.anime.title}", callback_data=f"show_actions:{entry.id}"))
    return builder.as_markup()

def get_detail_actions_keyboard(user_anime_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_entry:{user_anime_id}"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"confirm_delete:{user_anime_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_list_from_detail")
    )
    return builder.as_markup()

def get_confirm_delete_keyboard(user_anime_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"delete_confirmed:{user_anime_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data=f"delete_cancelled:{user_anime_id}")
    )
    return builder.as_markup()

# def get_anime_actions_keyboard(user_anime_id: int) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()

#     builder.row(
#         InlineKeyboardButton(text="✏️ Edit", callback_data=f"edit_anime:{user_anime_id}"),
#         InlineKeyboardButton(text="🗑️ Remove", callback_data=f"delete_anime:{user_anime_id}")
#     )

#     return builder.as_markup()
