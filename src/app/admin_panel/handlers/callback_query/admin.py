from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.keyboards.default.keyboard_generator import keyboards_generator
from src.core.filters.is_admin import IsAdmin
from src.app.product.handlers.commands.admin import add_product
from src.app.category.handlers.commands.admin import create_category


router = Router()


@router.callback_query(IsAdmin(), F.data == 'add_product')
async def command_add_product(query: types.CallbackQuery, state: FSMContext):
    await add_product(query.message, state)


@router.callback_query(IsAdmin(), F.data == 'add_category')
async def command_add_product(query: types.CallbackQuery, state: FSMContext):
    await create_category(query.message, state)


@router.callback_query(IsAdmin(), F.data.startswith('change_product_'))
async def command_change_product(query: types.CallbackQuery, state: FSMContext):
    product_id = query.data.split('_')[2]
    await state.set_state(AdminPanel.chose_product)
    await state.update_data(product_id=product_id)
    await query.message.answer(
        'Ви точно хочете змінити товар?',
        reply_markup=await inline_keyboards(
            yes='Так',
            no='Ні'
        )
    )


@router.callback_query(IsAdmin(), F.data == 'no')
async def command_no_change_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()


@router.callback_query(IsAdmin(), F.data == 'yes')
async def command_yes_change_product(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeProductStates.change_product)
    data = await state.get_data()
    product = await product_service.get(id=data['product_id'])
    await state.update_data(product=product)
