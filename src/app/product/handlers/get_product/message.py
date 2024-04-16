from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.app.product.handlers.utils.product import send_product_list
from src.app.product.states.search_product import SearchProduct
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator
from src.app.product.services.product import product_service

router = Router()


@router.message(F.text == 'Наявні товари')
async def send_product(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Введіть назву товару або натисніть на кнопку вивести вести товар',
        reply_markup=await inline_keyboards_generator(
            send_all_products='Вивести всі наявні товари'
        )
    )
    await state.set_state(SearchProduct.search)


@router.message(F.text, SearchProduct.search)
async def search_product(message: Message, state: FSMContext):
    query = await product_service.filter(name__icontains=message.text)
    await send_product_list(query, message)
    await state.clear()
