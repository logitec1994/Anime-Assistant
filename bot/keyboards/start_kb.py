"""
Inline клавиатуры для основного управления ботом
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура с основными действиями"""
    builder = InlineKeyboardBuilder()
    
    # Добавить
    builder.add(InlineKeyboardButton(
        text="➕ Добавить",
        callback_data="add_item"
    ))
    
    # Посмотреть список
    builder.add(InlineKeyboardButton(
        text="📋 Посмотреть список",
        callback_data="view_list"
    ))
    
    # Располагаем кнопки в одну строку
    builder.adjust(2)
    
    return builder.as_markup()
