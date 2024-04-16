import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.app.category.states.get_product_from_category import GetProductFromCategory
from src.app.product.services.product import product_service
from src.app.product.services.product_cart import ProductCard

callback_router = Router()


@callback_router.callback_query(F.data, GetProductFromCategory.get_product)
async def get_product_from_category(query: types.CallbackQuery, state: FSMContext):
    product_list_from_category = await product_service.get_category(category_id=query.data, in_storage=True)
    await state.clear()
    logging.debug(f'len: {len(product_list_from_category)}\n{product_list_from_category}')
    product_card = ProductCard(product_list_from_category, carousel=True, dp=callback_router)
    await query.message.answer_photo(**await product_card(user_id=query.from_user.id))
