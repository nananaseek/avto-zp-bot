from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.core.filters.is_admin import IsAdmin

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

command_router = Router()


@command_router.message(IsAdmin(), Command("addC"))
@command_router.message(IsAdmin(), Command("add_category"))
async def create_category(message: types.Message, state: FSMContext):
    await state.set_state(CreateCategory.name)
    await message.answer(answers.enter_category_name)
