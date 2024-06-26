from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.app.category.utils import category_utils
from src.core.filters.is_admin import IsAdmin
from src.app.product.states.add_product import AddProductState
from src.app.product import answers

router = Router()


@router.message(IsAdmin(), Command("addP"))
@router.message(IsAdmin(), Command("product"))
async def add_product(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != 'AddProductState:save_product':
        await state.clear()
        data = await state.update_data(is_correct=True)
        category_dict = await category_utils.get_category_and_inline(answers.enter_category_name, message)
        await state.update_data(category_dict=category_dict)

    await state.set_state(AddProductState.is_category)
