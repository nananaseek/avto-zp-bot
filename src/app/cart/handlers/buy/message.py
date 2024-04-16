import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.cart.services.cart import cart_service
from src.app.cart.services.order import order_service
from src.app.cart.state.cart import BuyProduct
from src.app.product.services.product import product_service
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.default.keyboard_generator import start_keyboard
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.utils.location import get_location

router = Router()


@router.message(F.text | F.location, BuyProduct.buy)
async def get_text_geo(message: types.Message, state: FSMContext):
    if message.location is not None:
        location = get_location(
            longitude=message.location.longitude,
            latitude=message.location.latitude
        )
    else:
        location = None
    await message.answer(
        f'Це коректна адреса:\n'
        f'{location or message.text}',
        reply_markup=await inline_keyboards(yes='Так, адреса вірна', no='Ні, переписати адресу')
    )
    await state.set_state(BuyProduct.check_address)
    await state.update_data(address=location or message.text)


@router.message(F.text, BuyProduct.check_address)
async def check_address_geo(message: types.Message, state: FSMContext):
    await get_text_geo(message, state)


@router.message(F.contact | F.text, BuyProduct.check_contact)
async def check_contact_user(message: types.Message, state: FSMContext):
    if message.contact is None:
        await message.answer('Відправте свої контакти чарез клавіатуру')
    else:
        admin = IsAdmin()
        await message.answer(
            'Замовлення відправленно у обробку',
            reply_markup=start_keyboard(is_admin=await admin(message)))
        state_data = await state.get_data()
        user_cart_data = await cart_service.carts(message.from_user.id)

        register_check = {
            'check_id': 0,
            'user_id': message.from_user.id,
            'chat_id': message.chat.id,
            'contact': message.contact,
            'address': state_data['address'],
            'username': message.from_user.username,
            'product': user_cart_data
        }
        await state.clear()
        await cart_service.delete_all_carts(message.from_user.id)
        for item in user_cart_data:
            is_correct = await product_service.buy_product(item['id'], int(item['takes_by_user']))
            if not is_correct:
                await message.answer('Оновіть корзину, деяких продуктів вже не має на складі')

        await order_service.save_check(**register_check)


