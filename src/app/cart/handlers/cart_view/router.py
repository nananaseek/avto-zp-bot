from aiogram import Router

from .message import router as message_router
from .callback_query import router as callback_router

cart_view_router = Router()

cart_view_router.include_routers(message_router, callback_router)
