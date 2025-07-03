# main.py
import asyncio
from aiogram import Bot, Dispatcher
from shared.config import BOT_TOKEN
from shared.log_config import setup_logging
from db.database import Database

from bot.handlers.common import router as common_router
from bot.handlers.add_anime import router as add_anime_router
from bot.handlers.list_anime import router as list_anime_router

async def main():
    # 1. Настраиваем логирование
    setup_logging()

    # 2. Инициализируем базу данных
    db = Database()
    db.create_tables()

    # 3. Инициализируем бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 4. Регистрируем роутеры
    dp.include_router(common_router)
    dp.include_router(add_anime_router)
    dp.include_router(list_anime_router)

    # 5. Передаем объект базы данных в хэндлеры через middleware (будет добавлено позже, пока вручную)
    # Сейчас мы передаем db_session как аргумент в хэндлер.
    # В будущем мы настроим Middleware для автоматической инъекции сессии.

    # 6. Запускаем polling
    try:
        # Для передачи db_session в хэндлеры, мы можем использовать dp.run_polling с state (context)
        # В aiogram v3 можно использовать Dependency Injection.
        # Пока мы просто передаем db объект в вызов run_polling,
        # а хэндлер будет получать его как db_session.
        await dp.start_polling(bot, db_session=db)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
