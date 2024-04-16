from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.app.product.handlers.utils.product import send_product_list
from src.app.product.services.product import product_service
from src.core.utils.dell_message import dell_two_message

router = Router()


@router.message(Command('send_all_products'))
async def send_all_products(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    product_list = await product_service.filter(quantity__gt=0)
    await dell_two_message(query.message.chat.id, query.message.message_id)
    await send_product_list(product_list, message=query.message, query=query)

