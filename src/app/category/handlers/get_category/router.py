from aiogram import Router

from .message import sub_message_router
from .callback_query import callback_router


get_category_router = Router(name=__name__)

get_category_router.include_routers(
    sub_message_router,
    callback_router
)
