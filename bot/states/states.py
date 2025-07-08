from aiogram.fsm.state import State, StatesGroup

class AddAnime(StatesGroup):
    waiting_for_title = State()
    waiting_for_status = State()
    waiting_for_current_episode = State()

class EditAnime(StatesGroup):
    choosing_field_to_edit = State()
    editing_status = State()
    editing_episode = State()
