from aiogram import Router

from .handlers.command import router as command_router
from .handlers.add_product_cart.router import add_product_cart_router
from .handlers.cart_view.router import cart_view_router

cart_router = Router()

cart_router.include_routers(command_router, add_product_cart_router, cart_view_router)
