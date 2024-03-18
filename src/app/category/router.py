from aiogram import Router

from src.app.category.handlers.commands.admin import sub_command_router
from src.app.category.handlers.call_back_query.admin import sub_callback_router

router = Router(name=__name__)

router.include_routers(sub_callback_router, sub_command_router)
