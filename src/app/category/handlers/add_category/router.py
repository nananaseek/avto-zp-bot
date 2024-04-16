from aiogram import Router

from .message import message_router
from .callback_query import callback_router
from .command import command_router

add_category_router = Router(name=__name__)

add_category_router.include_routers(
    message_router,
    callback_router,
    command_router
)
