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
