# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from bot.router import router
# from bot.middlewares.user_check import User
from aiogram.fsm.storage.memory import MemoryStorage
from core.db.engine import async_session

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register middlewares

    # Register routers
    dp.include_router(router)

    # Run the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
