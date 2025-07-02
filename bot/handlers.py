# bot/handlers.py
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from loguru import logger
from db.database import Database
from db.models import User, Anime, UserAnime, AnimeStatus
from bot.states import AddAnime
from bot.keyboards import get_anime_status_keyboard
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
        session.close()

@router.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} initiated adding anime.")
    await message.answer(f"Great! Which anime would you like to add? Type the title")
    await state.set_state(AddAnime.waiting_for_title)

@router.message(AddAnime.waiting_for_title)
async def process_anime_title(message: types.Message, state: FSMContext):
    anime_title = message.text.strip()
    if not anime_title:
        await message.answer("Please provide a valid anime title.")
        return
    
    await state.update_data(title=anime_title)
    logger.info(f"User {message.from_user.id} provided anime title: {anime_title}")
    await message.answer(
        f"Got it! You want to add anime: {anime_title}.", reply_markup=get_anime_status_keyboard()
    )

    await state.set_state(AddAnime.waiting_for_status)

@router.callback_query(AddAnime.waiting_for_status, F.data.startswith("set_status:"))
async def process_anime_status(callback: types.CallbackQuery, state: FSMContext, db_session: Database):
    status_str = callback.data.split(":")[1]
    anime_status = AnimeStatus(status_str)

    user_data = await state.get_data()
    anime_title = user_data.get('title')

    if not anime_title:
        logger(f"Error: Not found anime title in FSM Context")
        await callback.message.answer("An error occurred. Please try again.")
        await state.clear()
        return

    await state.update_data(status=anime_status)
    logger.info(f"User {callback.from_user.id} selected status: {anime_status.value} for anime: {anime_title}")

    if anime_status == AnimeStatus.WATCHING:
        await callback.message.answer(f"Great! Provide the number of episodes you have watched so far.")
        await state.set_state(AddAnime.waiting_for_current_episode)
    else:
        await callback.answer()
        await save_anime_to_db(callback.message, state, db_session)

@router.message(AddAnime.waiting_for_current_episode)
async def process_current_episode(message: types.Message, state: FSMContext):
    try:
        current_episode = int(message.text.strip())
        if current_episode < 0:
            raise ValueError("Episode number cannot be negative.")
        await state.update_data(current_episode=current_episode)
        logger.info(f"User {message.from_user.id} provided current episode: {current_episode}")
        await message.answer(f"Got it! Type 0 to finish adding or provide current episode time")
        await state.set_state(AddAnime.waiting_for_watched_time)
    except ValueError:
        await message.answer("Please provide a valid episode number.")

@router.message(AddAnime.waiting_for_watched_time)
async def process_watched_time(message: types.Message, state: FSMContext, db_session: Database):
    try:
        watched_time = int(message.text.strip())
        if watched_time < 0:
            raise ValueError("Watched time cannot be negative.")
        await state.update_data(watched_time_in_sec=watched_time)
        logger.info(f"User {message.from_user.id} provided watched time: {watched_time} seconds")
        await save_anime_to_db(message, state, db_session)
    except ValueError:
        await message.answer("Please provide a valid watched time in seconds.")

async def save_anime_to_db(message: types.Message, state: FSMContext, db_session: Database):
    user_data = await state.get_data()
    anime_title = user_data.get("title")
    anime_status = user_data.get("status")
    current_episode = user_data.get("current_episode", 0)
    watched_time_in_sec = user_data.get("watched_time_in_sec", 0)

    telegram_user_id = message.from_user.id
    
    try:
        user = db_session.get_user_by_telegram_id(telegram_user_id)
        if not user:
            logger.error(f"User {telegram_user_id} not found in database.")
            await message.answer("You need to start the bot first with /start command.")
            await state.clear()
            return
        
        anime = db_session.create_anime(title=anime_title)
        if not anime:
            logger.error(f"Failed to create/find anime with title: {anime_title}")
            await message.answer(f"Anime {anime_title} not found in database. Please check the title and try again.")
            await state.clear()
            return
        
        db_session.add_user_anime(
            user_id=user.id,
            anime_id=anime.id,
            status=anime_status,
            current_episode=current_episode,
            watched_time_in_sec=watched_time_in_sec
        )

        status_text = {
            AnimeStatus.TO_WATCH: "в список 'Буду смотреть'",
            AnimeStatus.WATCHING: "в список 'Смотрю сейчас'",
            AnimeStatus.WATCHED: "в список 'Просмотрено'",
            AnimeStatus.REWATCH: "в список 'Пересмотреть'",
        }.get(anime_status, "в ваш список")

        await message.answer(f"Anime {anime_title} successfully added {status_text}!")
        logger.info(f"Anime {anime_title} added for user {telegram_user_id} with status {anime_status.value}")
    except Exception as e:
        logger.error(f"Error saving anime {anime_title} for user {telegram_user_id}: {e}")
        await message.answer("An error occurrd while saving your anime. Please try again later.")
    finally:
        await state.clear()
