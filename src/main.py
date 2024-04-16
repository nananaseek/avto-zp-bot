from aiogram import F

from src.core.init import init_log_folder, configure_logging, dp, bot
from src.core.database.tortoise.db_config import db
from src.core.services.buy_invoice import invoice
from src.app.start_bot.start import router as start_router
from src.core.handlers.commands.general import router as general_commands_router
from src.core.handlers.commands.debug import router as debug_router
from src.app.admin_panel.router import router as admin_panel_router
from src.app.category.router import router as category_router
from src.app.product.router import product_router
from src.app.cart.router import cart_router


async def startup_bot() -> None:
    payment_handlers = invoice.reg_shipping_method()

    dp.startup.register(init_log_folder)
    dp.startup.register(configure_logging)
    dp.startup.register(db.startup)
    dp.shutdown.register(db.shutdown)

    dp.include_router(debug_router)
    dp.include_router(general_commands_router)

    dp.pre_checkout_query.register(payment_handlers['pre_checkout'])
    dp.message.register(payment_handlers['successful_message'], F.successful_payment)
    dp.shipping_query.register(payment_handlers['shipping_query'])

    dp.include_router(start_router)
    dp.include_router(admin_panel_router)
    dp.include_router(product_router)
    dp.include_router(category_router)
    dp.include_router(cart_router)

    await dp.start_polling(bot)
