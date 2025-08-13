from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shared.mappings import get_category_mappings, get_status_mappings

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
        [InlineKeyboardButton(text="✅ Да", callback_data="confirm_add")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="cancel_add")]
    ])

def items_list_keyboard(items: list) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{item.title}: {item.category}", callback_data=f"item_{item.id}")]
        for item in items
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def item_details_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Изменить статус", callback_data="change_status")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data="delete_item")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_list")]
    ])

def change_status_keyboard() -> InlineKeyboardMarkup:
    mappings = get_status_mappings()
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in mappings.values()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons, row_width=2)
