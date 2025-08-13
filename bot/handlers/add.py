from aiogram import Router, types, F
from bot.keyboards.inline_kb import category_keyboard, confirm_keyboard
from shared.fsm import AddItemFSM
from aiogram.fsm.context import FSMContext
from shared.mappings import get_category_mappings
from app.services.item_service import ItemService
from shared.dto import ItemCreateDTO
from database.session import get_db_session

router = Router()

def get_category_callback_data():
    return [callback_data[1] for callback_data in get_category_mappings().values()]

@router.callback_query(F.data == "add_item")
async def command_add_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Выбери категорию", reply_markup=category_keyboard())
    await state.set_state(AddItemFSM.waiting_for_category)

@router.callback_query(F.data.in_(get_category_callback_data()), AddItemFSM.waiting_for_category)
async def handle_category_selection(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    await state.set_state(AddItemFSM.waiting_for_title)
    await state.update_data(category=category)
    await callback.message.edit_text(f"Вы выбрали категорию: {category}. Теперь напишите название:")
    await callback.answer()

@router.message(F.text, AddItemFSM.waiting_for_title)
async def handle_title_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    title = message.text.strip()
    if not title:
        await message.answer("Название не может быть пустым.")
        return
    await state.update_data(title=title)
    await message.answer(f"{title}: {category} добавить?", reply_markup=confirm_keyboard())
    await state.set_state(AddItemFSM.waiting_for_confirmation)

@router.callback_query(F.data == "confirm_add", AddItemFSM.waiting_for_confirmation)
async def confirm_add_item(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')
    title = data.get('title')
    with get_db_session() as session:
        item_dto = ItemCreateDTO(title=title, category=category)
        item_service = ItemService(session)
        item = item_service.add_item(item_dto)
    await callback.answer(f"Добавлено: {item.title}: {item.category}")
    await callback.message.edit_text(f"Добавлено: {item.title}: {item.category}")
    await state.clear()

@router.callback_query(F.data == "cancel_add", AddItemFSM.waiting_for_confirmation)
async def cancel_add_item(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Добавление отменено.")
    data = await state.get_data()
    await state.clear()
    await callback.message.answer("Добавление было отменено.")
