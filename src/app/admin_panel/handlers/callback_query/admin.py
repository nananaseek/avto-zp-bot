import ast

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.admin_panel.states.admin_panel import OrderSend
from src.app.cart.services.order import order_service
from src.app.category.handlers.add_category.command import create_category
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards, \
    inline_pagination
from src.core.filters.is_admin import IsAdmin

router = Router()


@router.callback_query(IsAdmin(), F.data == 'add_category')
async def command_add_product(query: types.CallbackQuery, state: FSMContext):
    await create_category(query.message, state)


@router.callback_query(IsAdmin(), F.data == 'list_of_orders')
async def command_list_of_orders(query: types.CallbackQuery):
    data = await order_service.get_all_user_orders()
    if len(data) == 0:
        await query.message.answer('Ніхто не зробив замовлення :`)')
    else:
        kb_data = {
            f'user-order_{order['user_id']}_{order['check_id']}':
                f'Користувач: {order['username']} id: {order['check_id']}' for order in data
        }
        await query.message.answer(
            'Ось що замовляли та потрібно відправити',
            reply_markup=await inline_pagination(
                size=6,
                dp=router,
                **kb_data
            )
        )


@router.callback_query(IsAdmin(), F.data.startswith('user-order_'))
async def command_view_order(query: types.CallbackQuery):
    data = query.data.split('_')
    user_id = data[1]
    check_id = data[2]
    all_price = 0.00
    items = []

    order = await order_service.get_target_user_order(
        user_id=user_id,
        check_id=check_id
    )

    for item in ast.literal_eval(order['product']):
        price = float(item['new_price'])
        total_price = price * float(item['takes_by_user'])
        all_price += total_price
        name_item = (f'{item['name']}: \n'
                     f'{price:.2f}₴'
                     f' x '
                     f'{item['takes_by_user']}шт.'
                     f' = {total_price:.2f}₴\n')
        items.append(name_item)

    text = (f'Користувач {order['username']} замовив:\n\n'
            f'---\n'
            f'{'\n'.join(items)}'
            f'---\n'
            f'За адресою: \n'
            f'{order['address']}\n'
            f'---\n\n'
            f'Контакти користувача:\n'
            f'Ім\'я: {order['username']}\n'
            f'Телефон: {order['contact']}\n'
            f'---\n\n'
            f'Сумма до сплати користувача: {all_price:.2f}₴')

    kb = {
        f'send-message-to_{order['chat_id']}_{user_id}_{check_id}':
            'Надіслати користувачеві посилання для отримання замовлення',
        f'close_user_order': 'Закрити повідомлення'
    }

    await query.message.answer(
        text,
        reply_markup=await inline_keyboards(
            row=1,
            **kb
        )
    )


@router.callback_query(IsAdmin(), F.data == 'close_user_order')
async def close_user_order(query: types.CallbackQuery):
    await query.message.delete()


@router.callback_query(IsAdmin(), F.data.startswith('send-message-to_'))
async def take_info_for_user_message(query: types.CallbackQuery, state: FSMContext):
    data = query.data.split('_')
    await query.message.answer('Надішліть трек силку замовлення для користувача')
    await state.set_state(OrderSend.user_message)
    await state.update_data(chat_id=data[1], user_id=data[2], check_id=data[3])
