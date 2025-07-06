from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loguru import logger
from db.database import Database
from db.models import User, Anime, UserAnime, AnimeStatus
from bot.states import AddAnime
from bot.keyboards import get_anime_status_keyboard

router = Router()

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
        await save_anime_to_db(callback.message, state, db_session, telegram_user_id=callback.from_user.id)

@router.message(AddAnime.waiting_for_current_episode)
async def process_current_episode(message: types.Message, state: FSMContext, db_session: Database):
    try:
        current_episode = int(message.text.strip())
        if current_episode < 0:
            raise ValueError("Episode number cannot be negative.")
        await state.update_data(current_episode=current_episode)
        logger.info(f"User {message.from_user.id} provided current episode: {current_episode}")

        await save_anime_to_db(message, state, db_session, telegram_user_id=message.from_user.id)
    except ValueError:
        await message.answer("Please provide a valid episode number.")

async def save_anime_to_db(message: types.Message, state: FSMContext, db_session: Database, telegram_user_id: int):
    user_data = await state.get_data()
    anime_title = user_data.get("title")
    anime_status = user_data.get("status")
    current_episode = user_data.get("current_episode", 0)
    
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