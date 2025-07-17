import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, add
from service import MediaService
from repository import MediaRepository

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())

repo = MediaRepository()
service = MediaService(repo)

dp['service'] = service

dp.include_router(start.router)
dp.include_router(add.router)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
