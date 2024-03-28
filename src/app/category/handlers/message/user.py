from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.app.category.states.get_product_from_category import GetProductFromCategory
from src.app.category.utils import category_utils
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.filters.is_admin import IsAdmin

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

sub_message_router = Router()


@sub_message_router.message(IsAdmin(), F.text == 'Товар за категоріями')
async def chose_category(message: types.Message, state: FSMContext):
    await state.set_state(GetProductFromCategory.get_product)
    await category_utils.get_category_and_inline('Виберіть катенорію', message)
