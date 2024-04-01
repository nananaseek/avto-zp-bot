from aiogram import Router

from .handlers.add_product.router import add_product_router
from .handlers.get_product.router import get_product_router
from .handlers.change_product.router import change_product_router
from .handlers.delete_product.router import delete_product_router

product_router = Router()

product_router.include_routers(
    add_product_router,
    get_product_router,
    change_product_router,
    delete_product_router
)
