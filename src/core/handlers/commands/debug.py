import logging
import random

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.app.cart.services.cart import cart_service
from src.app.cart.services.order import order_service
from src.app.product.services.product import product_service
from src.app.product.services.product_cart import ProductCard
from src.core.filters.is_debug_mod import IsDebugMode
from src.core.filters.is_admin import IsAdmin
from src.core.init import dp
from src.core.services.buy_invoice import InvoicePay, invoice
from src.core.services.user import admin_service
from src.core.keyboards.inline.keyboard_generator import inline_pagination

router = Router()


@router.message(IsDebugMode(), IsAdmin(), Command('info'))
async def user_info(message: types.Message):
    is_admin = await admin_service.get(user_id=message.from_user.id)
    debug_user_info = (f"user_id: {message.from_user.id} \n"
                       f"first_name: {message.from_user.first_name}\n"
                       f"last_name: {message.from_user.last_name}\n"
                       f"username: {message.from_user.username}\n"
                       f"is_admin: {'False' if is_admin is None else 'True'}\n"
                       f"is_premium: {message.from_user.is_premium}\n")
    await message.answer(debug_user_info)


@router.message(IsDebugMode(), IsAdmin(), Command('inline_pagination_test'))
async def inline_pagination_test(message: types.Message, state: FSMContext):
    data = {str(random.randint(1, 100)): random.randint(1, 100) for _ in range(10)}
    await message.answer(
        'pagination test:',
        reply_markup=await inline_pagination(dp=router, size=3, **data)
    )


@router.message(IsDebugMode(), IsAdmin(), Command('carousel'))
async def carousel(message: types.Message, state: FSMContext):
    data = await product_service.all()
    # logging.debug(data)
    cart = await cart_service.carts(message.from_user.id)
    test = ProductCard(data=data, carousel=True, dp=router)
    a = await test(user_id=message.from_user.id)
    await message.answer_photo(**a)
    # for product in data:
    #     logging.debug(product)
    #
    #     test = ProductPagination(data=product, carousel=False, dp=router)
    #     a = test()
    #     await message.answer_photo(**a)


@router.message(IsDebugMode(), IsAdmin(), Command('cat'))
async def cat(message: types):
    test = await product_service.get_category('1')
    logging.debug(test)


@router.message(IsDebugMode(), IsAdmin(), Command('orders_test'))
async def orders_test(message: types.Message, state: FSMContext):
    data = await order_service.get_all_user_orders()
    logging.debug(data)
    kb_data = {
        f'user_{order['user_id']}': f'Користувач: {order['username']} id: {order['check_id']}' for order in data
    }
    await message.answer(
        'тест виводу замовлень',
        reply_markup=await inline_pagination(
            dp=router,
            **kb_data
        )
    )


@router.message(IsDebugMode(), IsAdmin(), Command('test_pay'))
async def test_pay(message: types.Message, state: FSMContext):
    data = await cart_service.carts(message.from_user.id)
    if len(data):
        await invoice(cart=data, message=message, photo_width=512, photo_height=248, picture=None)
    else:
        await message.answer('Спочатку заповніть корзину')
