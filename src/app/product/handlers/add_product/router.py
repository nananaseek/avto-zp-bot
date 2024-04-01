from aiogram import Router

from .callback_query import router as callback_query_router
from .command import router as command_router
from .message import router as message_router

add_product_router = Router()

add_product_router.include_routers(callback_query_router, command_router, message_router)
