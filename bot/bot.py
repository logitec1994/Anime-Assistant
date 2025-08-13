import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from bot.handlers import start
from bot.handlers import add

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(add.router)

# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
