from aiogram.filters import Command
from aiogram import Router, types

from dto import BaseDTO
from service import MediaService

router = Router()

@router.message(Command("add"))
async def cmd_add_media(message: types.Message, service: MediaService):
    title = "Some Anime Title"
    dto = BaseDTO(title=title)
    media = service.add_media(dto)
    await message.answer(f"Test")

    print(f"{media}")