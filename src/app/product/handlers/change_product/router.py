from aiogram import Router

from .callback_query import router as callback_router
from .message import router as message_router

change_product_router = Router()

change_product_router.include_routers(callback_router, message_router)