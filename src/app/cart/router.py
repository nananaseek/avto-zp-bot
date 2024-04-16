from aiogram import Router

from .handlers.add_product_cart.router import add_product_cart_router
from .handlers.cart_view.router import cart_view_router
from .handlers.buy.router import check_router

cart_router = Router()

cart_router.include_routers(
    add_product_cart_router,
    cart_view_router,
    check_router,
)
