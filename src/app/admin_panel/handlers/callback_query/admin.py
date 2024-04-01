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
from src.app.category.handlers.commands.admin import create_category


router = Router()


@router.callback_query(IsAdmin(), F.data == 'add_category')
async def command_add_product(query: types.CallbackQuery, state: FSMContext):
    await create_category(query.message, state)


