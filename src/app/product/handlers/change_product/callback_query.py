import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.category.utils import category_utils
from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product, change_product_from_queryset, \
    send_product_list
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState

router = Router()


@router.callback_query(IsAdmin(), F.data.startswith('change_'))
async def command_change_product(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    product_id = query.data.split('_')[1]
    await state.set_state(AdminPanel.chose_product)
    await state.update_data(product_id=product_id, message_id=query.message.message_id)
    # await query.message.answer(
    #     'Ви точно хочете змінити товар?',
    #     reply_markup=await inline_keyboards(
    #         yes='Так',
    #         no='Ні'
    #     )
    # )
    await state.set_state(ChangeProductStates.change_product)
    await state.update_data(message_id=query.message.message_id)
    await change_product_from_queryset(query.message, state)


@router.callback_query(IsAdmin(), AdminPanel.chose_product, F.data == 'no')
async def command_no_change_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()


@router.callback_query(IsAdmin(), AdminPanel.chose_product, F.data == 'yes')
async def command_yes_change_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(ChangeProductStates.change_product)
    await state.update_data(message_id=query.message.message_id)
    await change_product_from_queryset(query.message, state)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'name')
async def change_product_name(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(f'Введіть назву: ')
    await state.set_state(ChangeProductStates.name)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'description')
async def change_product_description(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введіть новий опис:')
    await state.set_state(ChangeProductStates.description)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'image')
async def change_product_image(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Відправте нову картинку:')
    await state.set_state(ChangeProductStates.image)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'price')
async def change_product_price(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введіть нову ціну:')
    await state.set_state(ChangeProductStates.price)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'quantity')
async def change_product_quantity(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введіть кількість:')
    await state.set_state(ChangeProductStates.quantity)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'discount')
async def change_product_discount(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Введіть нову скидку:')
    await state.set_state(ChangeProductStates.discount)


@router.callback_query(IsAdmin(), ChangeProductStates.change_product, F.data == 'close')
async def close_change_panel(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await send_product_list([data['product']], query.message, edit=True)
