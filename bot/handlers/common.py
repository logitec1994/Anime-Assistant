from aiogram import Router, types
from aiogram.filters import Command
from loguru import logger
from db.database import Database
from db.models import User

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, db_session: Database):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    session = next(db_session.get_db())

    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()

        if not user:
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
    except Exception as e:
        session.rollback()
        logger.error(f"Неожиданная ошибка при обработке /start для {user_id}: {e}")
        await message.answer("Произошла непредвиденная ошибка. Мы уже работаем над этим!")
    finally:
        session.close()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "Привет! Я NekoWatch, твой личный помощник по аниме. "
        "Я помогу тебе вести списки просмотренного и запланированного аниме.\n\n"
        "Вот что я умею:\n"
        "📜 */list* или */mylist* - Показать твои списки аниме. Ты можешь фильтровать их по категориям (Буду смотреть, Смотрю сейчас, Просмотрено, Пересмотреть).\n"
        "➕ */add* - Добавить новое аниме в свой список. Я спрошу название, статус и, если нужно, текущую серию/время.\n"
        "💡 */help* - Показать это сообщение с помощью.\n\n"
        "В будущем ты также сможешь редактировать записи, получать детализацию по аниме и делиться своими подборками!"
    )
    await message.answer(help_text, parse_mode="Markdown")
