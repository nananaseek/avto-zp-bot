from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.app.admin_panel.states.admin_panel import OrderSend
from src.app.cart.services.cart import cart_service
from src.app.cart.services.order import order_service
from src.app.product.services.product import product_service
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.filters.is_admin import IsAdmin
from src.core.utils.send_message import send_message_to_user

router = Router()


@router.message(IsAdmin(), F.text == 'Команди адміністратора')
async def admin_panel(message: types.Message):
    await message.delete()
    await message.answer(
        'Команди адміністратора',
        reply_markup=await inline_keyboards(
            row=2,
            add_product='Додати товар',
            add_category='Додати категорію',
            zero_quantity='Вивести товар якого не має на складі',
            list_of_orders='Вивести замовлення'
        )
    )


@router.message(IsAdmin(), F.text, OrderSend.user_message)
async def get_text_to_user_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = f'Ваше замовлення відправленно \nОсь посилання для відслідковування посилки {message.text}'

    await message.answer('Повідомлення користувачеві надіслано')
    await send_message_to_user(
        chat_id=data['chat_id'],
        text=text,
        # keyboard=InlineKeyboardMarkup(inline_keyboard=[
        #     [
        #         InlineKeyboardButton(
        #             text="Посилання для відслідковування",
        #             url=message.text,
        #             callback_data=None
        #         )
        #     ]
        # ])
    )
    await order_service.delete_user_order(user_id=data['user_id'], check_id=data['check_id'])
    await cart_service.delete_all_carts(data['user_id'])
    await state.clear()

