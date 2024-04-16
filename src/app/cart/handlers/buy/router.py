from aiogram import Router
from .message import router as message_router
from .callback import router as callback_router

check_router = Router()


check_router.include_routers(message_router, callback_router)
