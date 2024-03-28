from aiogram import Router

from src.app.category.handlers.commands.admin import sub_command_router
from src.app.category.handlers.callback_query.admin import sub_callback_router as admin_callback_router
from src.app.category.handlers.callback_query.user import sub_callback_router as user_callback_router
from src.app.category.handlers.message.user import sub_message_router as admin_message_router
from src.app.category.handlers.message.admin import sub_message_router as user_message_router

router = Router(name=__name__)

router.include_routers(
    admin_callback_router,
    user_callback_router,
    sub_command_router,
    admin_message_router,
    user_message_router

)
