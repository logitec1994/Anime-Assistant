from aiogram.filters import Command
from aiogram.types import Message

from aiogram import Router

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")
