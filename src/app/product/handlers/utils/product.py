import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from src.app.category.services.category import category_service
from src.app.product import answers
from src.app.product.schemas.product import Pydantic_Product_Create
from src.app.product.services.product import product_service
from src.app.product.states.add_product import AddProductState
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards


async def save_product(data: dict, message: types.Message, state: FSMContext):
    category = data.pop('category')
    data.pop('is_correct')
    data.pop('category_dict')
    try:
        schema = Pydantic_Product_Create(**data)
        product = await product_service.create(schema)

        await category_service.add_product_to_category(
            category_id=category,
            product=product
        )

        await message.answer(answers.product_is_created)
    except ValidationError as e:
        await message.answer(answers.create_product_error)
        logging.error(e)
    finally:
        await state.clear()


async def change_product(data: dict, message: types.Message, state: FSMContext):
    await state.set_state(AddProductState.save_product)
    data.pop('is_correct')
    c_dict = data.pop('category_dict')
    data['category'] = 'Категорія: ' + c_dict[f'{data["category"]}']
    data['name'] = f'Назва: {data["name"]}'
    data['description'] = f'Опис: {data["description"]}'
    data['image'] = answers.change_image_product
    if data['discount'] is None:
        data['discount'] = 'На продукт не має знижки'
    elif data['discount']:
        data['discount'] = f'Знижка: {data["discount"]}%'
    data['price'] = f'Ціна: {data["price"]}₴'
    data['quantity'] = f'Товару на складі: {data["quantity"]}шт'
    await message.answer_photo(
        data['image'],
        caption=answers.is_correct_product_data,
        reply_markup=await inline_keyboards(
            **data,
            create_product=answers.create_product
        )
    )
