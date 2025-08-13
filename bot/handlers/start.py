from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.inline_kb import start_keyboard

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: types.Message) -> None:
    await message.answer("Привет! Я помогу тебе не забыть ни одно аниме или мангу. 🎬📖\nПросто напиши название - я добавлю его в список.", reply_markup=start_keyboard())
