from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.app.category.states.get_product_from_category import GetProductFromCategory
from src.app.category.utils import category_utils


sub_message_router = Router()


@sub_message_router.message(F.text == 'Товар за категоріями')
async def chose_category(message: types.Message, state: FSMContext):
    await state.set_state(GetProductFromCategory.get_product)
    await category_utils.get_category_and_inline('Виберіть катенорію', message)
