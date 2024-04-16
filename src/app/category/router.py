from aiogram import Router

from .handlers.get_category.router import get_category_router
from .handlers.add_category.router import add_category_router

router = Router(name=__name__)

router.include_routers(
    get_category_router,
    add_category_router
)
