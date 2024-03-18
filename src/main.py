from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from src.core.init import init_log_folder, configure_logging
from src.settings.config import settings
from src.core.database.db_config import db
from src.app.start_bot.start import router as start_router
from src.core.handlers.commands.general import router as general_commands_router
from src.core.handlers.commands.debug import router as debug_router
from src.app.category.router import router as category_router
from src.app.product.router import router as add_product_router

dp = Dispatcher()


async def startup_bot() -> None:
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.HTML)

    dp.startup.register(init_log_folder)
    dp.startup.register(configure_logging)
    dp.startup.register(db.startup)
    dp.shutdown.register(db.shutdown)

    dp.include_router(debug_router)
    dp.include_router(general_commands_router)

    dp.include_router(start_router)
    dp.include_router(add_product_router)
    dp.include_router(category_router)
    await dp.start_polling(bot)
