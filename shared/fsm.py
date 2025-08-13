from aiogram.fsm.state import State, StatesGroup

class AddItemFSM(StatesGroup):
    waiting_for_category = State()
    waiting_for_title = State()
    waiting_for_confirmation = State()
