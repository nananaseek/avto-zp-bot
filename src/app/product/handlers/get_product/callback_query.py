from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.product.handlers.utils.product import send_product_list
from src.app.product.services.product import product_service
from src.app.product.states.search_product import SearchProduct
from src.core.filters.is_admin import IsAdmin
from src.core.utils.dell_message import dell_two_message

router = Router()


@router.callback_query(F.data == 'send_all_products', SearchProduct.search)
async def send_all_products(query: types.CallbackQuery, state: FSMContext):
    product_list = await product_service.filter(quantity__gt=0)
    await state.clear()
    await dell_two_message(query.message.chat.id, query.message.message_id)
    await send_product_list(product_list, message=query.message, query=query)


@router.callback_query(F.data == 'zero_quantity', IsAdmin())
async def zero_quantity(query: types.CallbackQuery):
    product_list = await product_service.filter(quantity=0)
    if len(product_list) == 0:
        await query.message.answer('Весь товар є в наявності')
    else:
        await send_product_list(product_list, query.message)
