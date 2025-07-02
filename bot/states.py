from aiogram.fsm.state import State, StatesGroup

class AddAnime(StatesGroup):
    waiting_for_title = State()
    waiting_for_status = State()
    waiting_for_current_episode = State()
    waiting_for_watched_time = State()
