from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.cart.state.cart import ChooseState
from src.app.product.handlers.utils.product import change_cart_product
from src.core.keyboards.inline.keyboard_generator import inline_pagination
from src.core.utils.dell_message import dell_two_message
from src.app.cart.services.cart import cart_service
from src.core.utils.edit_media import edit_text

router = Router()


@router.message(F.text == 'Корзина')
async def cart_view(message: types.Message):
    data = await cart_service.carts(message.from_user.id)
    if len(data) > 0:
        all_price = 0.00
        items = []

        for item in data:
            price = float(item['new_price'])
            total_price = price * float(item['takes_by_user'])
            all_price += total_price
            name_item = (f'{item['name']}: \n'
                         f'{price:.2f}₴'
                         f' x '
                         f'{item['takes_by_user']}шт.'
                         f' = {total_price:.2f}₴\n')
            items.append(name_item)

        choose_item = {f'cart-item_{item['id']}': item['name'] for item in data}
        text = (f'Корзина:\n'
                f'---\n'
                f'{'\n'.join(items)}'
                f'---\n'
                f'Зашалом: {all_price:.2f}₴')

        await message.answer(
            text,
            reply_markup=await inline_pagination(
                size=6,
                **choose_item, clean_carts='Очистити корзину', buy='Оформити замовлення'
            )
        )
    else:
        await message.answer('В корзині не має товару')


@router.message(ChooseState.amount, F.text)
async def choose_amount(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        amount = int(message.text)
        data = await state.get_data()
        await edit_text(
            'Добренько:)',
            keyboard=None,
            message_id=message.message_id - 1,
            chat_id=message.chat.id
        )

        product = await cart_service.get_product_from_cart(message.from_user.id, data['product_id'])

        if product is None:
            await message.answer('Помилка, додайте продукт в корзину заново')
        else:
            is_added = await cart_service.add_product_to_cart(message.from_user.id, data['product_id'], amount=amount)

            if is_added:
                added_product = await cart_service.get_product_from_cart(message.from_user.id, data['product_id'])
                await change_cart_product(added_product, data['message'], edit=True)
            else:
                await message.answer('Неможливо додати ще товару бо такої кількості не має на складі')

        await state.clear()
        await dell_two_message(message.chat.id, message.message_id)

    else:
        await message.delete()
        await edit_text(
            'Кількість має бути в цифрах',
            keyboard=None,
            message_id=message.message_id - 1,
            chat_id=message.chat.id
        )
