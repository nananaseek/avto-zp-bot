from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.app.product.services.product import product_service

router = Router()


@router.message(F.text == 'Наявні товари')
async def send_product(message: Message, state: FSMContext):
    product_list = await product_service.all()

    await message.delete()
    await message.answer('Ось наявні товари')

    for product in product_list:
        if product.discount is None:
            is_discount = product.price
        else:
            new_price = product.price - (product.price * product.discount / 100)
            is_discount = f'<s>{product.price}₴</s> {new_price:.2f}₴'

        await message.answer_photo(
            product.image,
            caption=f'Назва продукту: {product.name} \n'
                    f'Опис продукту: {product.description}\n'
                    f'Ціна: {is_discount}\n'
                    f'Кількість на складі: {product.quantity}шт',
            parse_mode=ParseMode.HTML
        )

