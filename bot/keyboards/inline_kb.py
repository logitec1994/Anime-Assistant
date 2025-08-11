from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shared.mappings import get_cetegory_mappings

def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить", callback_data="add_item")],
        [InlineKeyboardButton(text="📜 Список", callback_data="list_items")]
    ])

def category_keyboard() -> InlineKeyboardMarkup:
    mappings = get_cetegory_mappings()
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in mappings.values()
    ]    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
