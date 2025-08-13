from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shared.mappings import get_category_mappings

def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить", callback_data="add_item")],
        [InlineKeyboardButton(text="📜 Список", callback_data="list_items")]
    ])

def category_keyboard() -> InlineKeyboardMarkup:
    mappings = get_category_mappings()
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in mappings.values()
    ]    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="confirm_add")],
        [InlineKeyboardButton(text="Нет", callback_data="cancel_add")]
    ])
