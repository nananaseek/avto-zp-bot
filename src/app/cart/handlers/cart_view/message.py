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
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards, \
    inline_pagination
from src.app.product.states.add_product import AddProductState
from src.core.utils.dell_message import dell_target_message
from src.app.cart.services.cart import cart_service

router = Router()


@router.message(F.text == 'Корзина')
async def cart_view(message: types.Message, state: FSMContext):
    data = await cart_service.carts(message.from_user.id)
    logging.debug(len(data) > 0)
    if len(data) > 0:
        all_price = 0.00
        items = []

        for item in data:
            price = float(item['price'])
            total_price = price * float(item['takes_by_user'])
            all_price += price
            name_item = (f'{item['name']} '
                         f'{price:.2f}'
                         f'x'
                         f'{item['takes_by_user']}'
                         f' = {total_price:.2f}₴')
            items.append(name_item)

        choose_item = {f'cart-item_{item['id']}': item['name'] for item in data}
        text = (f'Товар в корзині:\n'
                f'{'\n'.join(items)}\n'
                f'----------------------------\n'
                f'обща ціна: {all_price:.2f}₴')

        await message.answer(
            text,
            reply_markup=await inline_pagination(
                size=6,
                **choose_item
            )
        )
    else:
        await message.answer('В корзині не має товару')
