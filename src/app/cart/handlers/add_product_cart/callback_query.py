import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.category.utils import category_utils
from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product, change_product_from_queryset, \
    send_product_list
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState
from src.core.utils.dell_message import dell_target_message
from src.app.cart.services.cart import cart_service

router = Router()


@router.callback_query(F.data.startswith('to-cart'))
async def add_to_cart(query: CallbackQuery, state: FSMContext):
    product_data = query.data.split('_')
    logging.debug(product_data[1])
    product = await product_service.get(id=product_data[1])
    if product.discount is None:
        is_discount = product.price
    else:
        is_discount = product.price - (product.price * product.discount / 100)

    to_cart = {
        'user_id': query.from_user.id,
        'id': product.id,
        'image': product.image,
        'name': product.name,
        'description': product.description,
        'price': is_discount,
        'quantity': product.quantity,
        'takes_by_user': 1
    }
    is_add = await cart_service.save_cart(**to_cart)
    await query.message.answer(
        'Товар додано до корзини'
        if is_add else
        'Неможливо додати ще товару бо такої кількості не має на складі'
    )
