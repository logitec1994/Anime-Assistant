from aiogram import Router, types, F
from app.services.item_service import ItemService
from database.session import get_db_session
from bot.keyboards.inline_kb import items_list_keyboard, item_details_keyboard

router = Router()

@router.callback_query(F.data == "list_items")
async def command_list_handler(callback: types.CallbackQuery):
    await callback.answer("Получение списка...")
    db_session = get_db_session()
    items = ItemService(db_session).get_items()
    if not items:
        await callback.message.answer("Ничего в базе нет.")
        return
    await callback.message.answer("Текущий список.", reply_markup=items_list_keyboard(items))

@router.callback_query(F.data.startswith("item_"))
async def item_selected_handler(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    with get_db_session() as db_session:
        item = ItemService(db_session).get_item_by_id(item_id)
    if not item:
        await callback.answer("Элемент не найден.")
        return
    await callback.message.edit_text(item.title, reply_markup=item_details_keyboard())