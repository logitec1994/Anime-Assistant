from aiogram import Router, types
from aiogram.filters import Command

add_router = Router()

@add_router.message(Command("add"))
async def start_adding(message: types.Message):
    await message.answer("Its works!")