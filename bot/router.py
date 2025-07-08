from aiogram import Router

from bot.handlers.media.add import add_router

router = Router()

router.include_router(add_router)
