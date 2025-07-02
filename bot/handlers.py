# bot/handlers.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from loguru import logger
from db.database import Database
from db.models import User # Импортируем модель User
from sqlalchemy.exc import IntegrityError # Для обработки ошибок уникальности

# Создаем роутер для обработки команд и сообщений
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, db_session: Database):
    """
    Обработчик команды /start.
    Регистрирует нового пользователя или приветствует существующего.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    session = next(db_session.get_db()) # Получаем сессию базы данных

    try:
        # Пытаемся найти пользователя по telegram_id
        user = session.query(User).filter_by(telegram_id=user_id).first()

        if not user:
            # Если пользователя нет, создаем нового
            new_user = User(
                telegram_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            logger.info(f"Новый пользователь зарегистрирован: {new_user.telegram_id}")
            await message.answer(
                f"Привет, {message.from_user.full_name}! 👋\n"
                "Добро пожаловать в NekoWatch — твоего личного помощника по аниме! "
                "Я помогу тебе вести списки просмотренного и запланированного аниме."
            )
        else:
            logger.info(f"Существующий пользователь вернулся: {user.telegram_id}")
            await message.answer(
                f"Снова привет, {message.from_user.full_name}! 👋\n"
                "Рад тебя видеть в NekoWatch! Чем могу помочь?"
            )
    except IntegrityError:
        session.rollback() # Откатываем транзакцию в случае ошибки
        logger.error(f"Ошибка при регистрации пользователя {user_id}: конфликт ID.")
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.")
    except Exception as e:
        session.rollback()
        logger.error(f"Неожиданная ошибка при обработке /start для {user_id}: {e}")
        await message.answer("Произошла непредвиденная ошибка. Мы уже работаем над этим!")
    finally:
        session.close() # Закрываем сессию
