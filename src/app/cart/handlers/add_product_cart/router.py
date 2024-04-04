from aiogram import Router

from .callback_query import router as callback_router

add_product_cart_router = Router()

add_product_cart_router.include_routers(callback_router,)
