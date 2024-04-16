import time

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.cart.services.order import order_service
from src.app.cart.state.cart import BuyProduct
from src.app.cart.services.cart import cart_service
from src.core.keyboards.default.keyboard_generator import contact_keyboard
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator
from src.core.services.buy_invoice import invoice

router = Router()


@router.callback_query(F.data == 'buy')
async def buy(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(
        'Виберіть метод оплати',
        reply_markup=await inline_keyboards_generator(
            online_pay='Оплатити онлайн',
            offline_pay='Оплата при оформленні'
        )
    )


@router.callback_query(F.data == 'online_pay')
async def online_pay(query: types.CallbackQuery, state: FSMContext):
    data = await cart_service.carts(query.from_user.id)
    if len(data):
        await invoice(
            cart=data,
            user_id=query.from_user.id,
            message=query.message,
            photo_width=512,
            photo_height=248,
            picture=None
        )
    else:
        await query.message.answer('Спочатку заповніть корзину')


@router.callback_query(F.data == 'offline_pay')
async def offline_pay(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(
        'Відправте геоданні до пункту видачі з якого вам буде зручно отримати посилання :), або напишіть його адресу\n'
        'Ваше замовлення прийде в той пункт видачі який був найближчим до вибраного вами місця\n\n'
    )
    time.sleep(1)
    await query.message.answer(
        'Дочекайтеся поки адміністратор обробить замовлення, вам надійде повідомлення про успашну відправку замовлення'
    )
    await state.set_state(BuyProduct.buy)


@router.callback_query(F.data == 'no', BuyProduct.check_address)
async def change_address(query: types.CallbackQuery):
    await query.message.answer('Відправте нову адресу')


@router.callback_query(F.data == 'yes', BuyProduct.check_address)
async def save_address(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(
        'Тепер відправте свої контакти, щоб з вами зміг зв\'язатися ваш персональний адміністратор',
        reply_markup=contact_keyboard()
    )
    await state.set_state(BuyProduct.check_contact)

