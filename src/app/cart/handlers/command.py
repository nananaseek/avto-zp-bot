import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

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


@router.message(Command('test_cart_save'))
async def test_cart_save(message: types.Message, state: FSMContext):
    product = await product_service.get(id='39d97f89-eb9d-4b65-8d6a-6a651ee78277')
    product_to_cart = {
        'id': product.id,
        'name': product.name,
        'image': product.image,
        'price': product.price,
        'quantity': 1
    }
    product.update(user_id=message.from_user.id)
    await cart_service.save_cart(**product)
    cart = await cart_service.carts(message.from_user.id)
    await message.answer(f'{dict(cart[0])["name"]}')
    # await message
