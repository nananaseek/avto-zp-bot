import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto
from pydantic import ValidationError

from src.app.cart.services.cart import cart_service
from src.app.category.services.category import category_service
from src.app.product import answers
from src.app.product.schemas.product import Pydantic_Product_Create
from src.app.product.services.product import product_service
from src.app.product.states.add_product import AddProductState
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.utils.edit_media import edit_photo


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
    logging.info(str(data))
    data.pop('is_correct')
    photo = data.pop('image')
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
        photo,
        caption=answers.is_correct_product_data,
        reply_markup=await inline_keyboards(
            **data,
            create_product=answers.create_product
        )
    )


async def change_product_from_queryset(message: types.Message, state: FSMContext):
    await state.set_state(ChangeProductStates.change_product)
    data = await state.get_data()
    product = await product_service.get(obj=True, id=data['product_id'])
    product_category = await product.categories.all().first()
    await state.update_data(product=product, category=product_category)
    product, category = (await product_service.obj_to_schema(product),
                         await category_service.obj_to_schema(product_category))
    product_schema, category_schemas = product.model_dump(), category.model_dump()

    is_discount = 'Знижки на товар не має' if product_schema['discount'] is None else f'Знижка: {product_schema['discount']}%'

    callback_data_kb = {
        f'name': f'Назва: {product_schema['name']}',
        f'description': f'Опис: {product_schema['description']}',
        f'image': 'Змінити картинку?',
        f'price': f'Ціна: {product_schema['price']}',
        f'quantity': f'Кількість: {product_schema['quantity']}',
        f'discount': is_discount,
        f'close': 'Завершити редагування.'}

    kb = await inline_keyboards(
        # category=f'Категорія: {category_schemas['name']}',
        **callback_data_kb
    )
    if 'in_change' in data:
        await edit_photo(
            image=product_schema['image'],
            text=f'Виберіть що хочете змінити \nsave {data['message_id']}\n {message.message_id}',
            keyboard=kb,
            chat_id=message.chat.id,
            message_id=message.message_id - data['counter']
        )
        await state.update_data(counter=data['counter'] + 2)

    else:
        await message.answer_photo(
            product_schema['image'],
            caption=f'Виберіть що хочете змінити\n {message.message_id}',
            reply_markup=kb
        )
        await state.update_data(in_change=True, message_id=message.message_id, counter=2)


async def send_product_list(
        product_list,
        message: types.Message,
        query: types.CallbackQuery = None,
        edit=None,
        carousel=True
):
    is_admin = IsAdmin()
    for product in product_list:
        if product.discount is None:
            is_discount = product.price
        else:
            new_price = product.price - (product.price * product.discount / 100)
            is_discount = f'<s>{product.price}₴</s> {new_price:.2f}₴'

        if await is_admin(message if query is None else query.message):
            id_product = {
                f'change_{product.id}': 'Редагувати продукт',
                f'delete_{product.id}': 'Видалити продукт'
            }
        else:
            is_product = await cart_service.get_product_from_cart(
                message.from_user.id if query is None else query.from_user.id,
                product.id
            )
            if is_product is None:
                id_product = {
                    f'to-cart_{product.id}': 'До корзини'
                }
            else:
                id_product = {
                    f'increase_{product.id}': '+1',
                    f'choose-amount_{product.id}': f'✏️ {is_product['takes_by_user']}шт.',
                    f'decrease_{product.id}': '-1',
                }

        if edit is None:
            await message.answer_photo(
                product.image,
                caption=f'Назва продукту: {product.name} \n'
                        f'Опис продукту: {product.description}\n'
                        f'Ціна: {is_discount}\n'
                        f'Кількість на складі: {product.quantity}шт',
                parse_mode=ParseMode.HTML,
                reply_markup=await inline_keyboards(
                    row=3,
                    **id_product
                )
            )
        else:
            await message.edit_media(
                InputMediaPhoto(
                    media=product.image,
                    caption=f'Назва продукту: {product.name} \n'
                            f'Опис продукту: {product.description}\n'
                            f'Ціна: {is_discount}\n'
                            f'Кількість на складі: {product.quantity}шт',
                    parse_mode=ParseMode.HTML,
                ),
                reply_markup=await inline_keyboards(
                    row=3,
                    **id_product
                ) if await is_admin(message) else None
            )


async def change_cart_product(product: dict, message: types.Message, edit: bool = False):
    id_product = {
        f'increase_{product['id']}': '+1',
        f'choose-amount_{product['id']}': f'✏️ {product['takes_by_user']}шт.',
        f'decrease_{product['id']}': '-1',
    }
    if product['discount'] == '0':
        is_discount = product['price']
    else:
        is_discount = f'<s>{float(product['price']):.2f}₴</s> {float(product['new_price']):.2f}'

    text = (f'Назва продукту: {product['name']} \n'
            f'Опис продукту: {product['description']}\n'
            f'Ціна: {is_discount}₴\n'
            f'Кількість на складі: {product['quantity']}шт\n')

    if edit:
        await message.edit_media(
            InputMediaPhoto(
                media=product['image'],
                caption=text
            ),
            reply_markup=await inline_keyboards(row=3, **id_product)
        )
    else:
        await message.answer_photo(
            product['image'],
            caption=text,
            reply_markup=await inline_keyboards(row=3, **id_product)
        )