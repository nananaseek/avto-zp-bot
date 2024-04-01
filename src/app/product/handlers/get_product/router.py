from aiogram import Router

from .message import router as message_router
from .callback_query import router as callback_router

get_product_router = Router()
get_product_router.include_routers(message_router, callback_router)