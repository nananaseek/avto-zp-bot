import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from pydantic import ValidationError

from src.app.category.services.category import category_service
from src.app.product import answers
from src.app.product.schemas.product import Pydantic_Product_Create
from src.app.product.services.product import product_service
from src.app.product.states.add_product import AddProductState
from src.core.filters.is_admin import IsAdmin
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


async def change_product_from_data(data: dict, message: types.Message, state: FSMContext):
    await state.set_state(AddProductState.save_product)
    data.pop('is_correct')
    c_dict = data.pop('category_dict')
    photo = data['image']
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
        photo,
        caption=answers.is_correct_product_data,
        reply_markup=await inline_keyboards(
            **data,
            create_product=answers.create_product
        )
    )


# async def change_product_from_queryset()


async def send_product_list(product_list, message: types.Message):
    is_admin = IsAdmin()
    for product in product_list:
        if product.discount is None:
            is_discount = product.price
        else:
            new_price = product.price - (product.price * product.discount / 100)
            is_discount = f'<s>{product.price}₴</s> {new_price:.2f}₴'

        id_product = {
            f'change_product_{product.id}': 'Редагувати продукт',
            f'delete_product_{product.id}': 'Видалити продукт'
        }

        await message.answer_photo(
            product.image,
            caption=f'Назва продукту: {product.name} \n'
                    f'Опис продукту: {product.description}\n'
                    f'Ціна: {is_discount}\n'
                    f'Кількість на складі: {product.quantity}шт',
            parse_mode=ParseMode.HTML,
            reply_markup=await inline_keyboards(
                **id_product
            ) if await is_admin(message) else None
        )
