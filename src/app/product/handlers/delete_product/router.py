from aiogram import Router

from .callback_query import router as callback_query_router

delete_product_router = Router()

delete_product_router.include_routers(callback_query_router)
