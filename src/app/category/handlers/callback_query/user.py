import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.category.schemas.category import Pydantic_Category_Create
from src.app.category.services.category import category_service

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers
from src.app.category.states.get_product_from_category import GetProductFromCategory
from src.app.product.handlers.utils.product import send_product_list
from src.app.category.services.category import category_service
from src.app.product.schemas.product import Pydantic_Product_Get

sub_callback_router = Router()


@sub_callback_router.callback_query(F.data, GetProductFromCategory.get_product)
async def get_product_from_category(query: types.CallbackQuery, state: FSMContext):
    select_category = await category_service.filter(obj=True, id=query.data)
    category_product_list = await select_category.prefetch_related('product_categories')
    category_product = await category_product_list[0]
    await send_product_list(category_product.product_categories, message=query.message)
