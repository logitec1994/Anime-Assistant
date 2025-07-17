from aiogram.filters import Command
from aiogram import Router, types, html

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")