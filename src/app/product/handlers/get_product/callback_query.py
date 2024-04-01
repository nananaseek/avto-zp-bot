import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product, send_product_list
from src.app.product.services.product import product_service
from src.app.product.states.search_product import SearchProduct
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState

router = Router()


@router.callback_query(F.data == 'send_all_products', SearchProduct.search)
async def send_all_products(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    product_list = await product_service.filter(quantity__gt=0)
    await send_product_list(product_list, query.message)


@router.callback_query(IsAdmin(), F.data == 'zero_quantity')
async def zero_quantity(query: types.CallbackQuery, state: FSMContext):
    product_list = await product_service.filter(quantity=0)
    if len(product_list) == 0:
        await query.message.answer('Весь товар є в наявності')
    else:
        await send_product_list(product_list, query.message)
