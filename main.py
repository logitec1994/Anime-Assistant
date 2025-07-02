# main.py
import asyncio
from aiogram import Bot, Dispatcher
from shared.config import BOT_TOKEN
from shared.log_config import setup_logging
from db.database import Database
from bot.handlers import router as user_router # Импортируем роутер

async def main():
    # 1. Настраиваем логирование
    setup_logging()

    # 2. Инициализируем базу данных
    db = Database()
    db.create_tables()

    # 3. Инициализируем бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 4. Регистрируем роутер с хэндлерами
    dp.include_router(user_router)

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
        await bot.session.close() # Закрываем сессию бота при завершении

if __name__ == "__main__":
    asyncio.run(main())
