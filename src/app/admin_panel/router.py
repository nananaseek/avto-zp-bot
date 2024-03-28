from aiogram import Router

from src.app.admin_panel.handlers.message.admin import router as admin_panel_message_router
from src.app.admin_panel.handlers.callback_query.admin import router as admin_panel_callback_query_router

router = Router()

router.include_routers(
    admin_panel_callback_query_router,
    admin_panel_message_router
)
