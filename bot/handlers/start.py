from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Я помогу тебе не забыть ни одно аниме или мангу. 🎬📖\nПросто напиши название - я добавлю его в список.")
