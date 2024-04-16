from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.app.cart.utils.product_to_cache import get_product_to_cache
from src.app.product.handlers.utils.product import change_cart_product
from src.app.cart.services.cart import cart_service

router = Router()


@router.callback_query(F.data.startswith('to-cart'))
async def add_to_cart(query: CallbackQuery):
    product_id = query.data.split('_')[1]
    user_id = query.from_user.id
    is_add = await get_product_to_cache(product_id, user_id)
    if is_add:
        product = await cart_service.get_product_from_cart(user_id=user_id, uuid=product_id)
        await change_cart_product(product, query.message, edit=True)
        await query.answer('Товар додано до корзини')
    else:
        await query.answer(
            'Неможливо додати ще товару бо такої кількості не має на складі'
        )
