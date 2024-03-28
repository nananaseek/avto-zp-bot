from aiogram import Router

from src.app.product.handlers.callback_query.admin import router as callback_admin_router
from src.app.product.handlers.callback_query.user import router as callback_user_router
from src.app.product.handlers.commands.admin import router as command_admin_router
from src.app.product.handlers.message.admin import router as message_admin_router
from src.app.product.handlers.message.user import router as message_user_router
router = Router()

router.include_routers(
    callback_admin_router,
    callback_user_router,
    command_admin_router,
    message_admin_router,
    message_user_router
)
