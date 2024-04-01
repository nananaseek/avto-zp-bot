import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.category.utils import category_utils
from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product, change_product_from_queryset
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState


router = Router()


@router.callback_query(IsAdmin(), F.data.startswith('delete_'))
async def command_change_product(query: types.CallbackQuery, state: FSMContext):
    product_id = query.data.split('_')[1]
    await state.set_state(AdminPanel.remove_product)
    await state.update_data(product_id=product_id)
    await query.message.answer(
        'Ви точно хочете видалити товар?',
        reply_markup=await inline_keyboards(
            yes='Так',
            no='Ні'
        )
    )


@router.callback_query(IsAdmin(), AdminPanel.remove_product, F.data == 'no')
async def command_no_change_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()


@router.callback_query(IsAdmin(), AdminPanel.remove_product, F.data == 'yes')
async def command_yes_change_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    data = await state.get_data()
    await product_service.delete(id=data['product_id'])
    await query.answer('Товар видалено!')
    