"""
Обработчик команды /start и callback-запросов
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.start_kb import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    welcome_text = """
🎌 <b>Добро пожаловать в Anime Assistant!</b>

Выберите действие:
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == "add_item")
async def add_item_handler(callback: CallbackQuery):
    """Обработчик кнопки 'Добавить'"""
    await callback.message.edit_text(
        "➕ <b>Добавить элемент</b>\n\nФункция в разработке...",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "view_list")
async def view_list_handler(callback: CallbackQuery):
    """Обработчик кнопки 'Посмотреть список'"""
    await callback.message.edit_text(
        "📋 <b>Список элементов</b>\n\nФункция в разработке...",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()
