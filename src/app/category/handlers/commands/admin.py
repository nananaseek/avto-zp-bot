from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.filters.is_admin import IsAdmin

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

sub_command_router = Router()


@sub_command_router.message(IsAdmin(), Command("addC"))
@sub_command_router.message(IsAdmin(), Command("add_category"))
async def create_category(message: types.Message, state: FSMContext):
    await state.set_state(CreateCategory.name)
    await message.answer(answers.enter_category_name)


@sub_command_router.message(IsAdmin(), CreateCategory.name)
async def add_name(message: types.Message, state: FSMContext):
    data = await state.update_data(name=message.text)

    await message.answer(
        answers.edit_category,
        reply_markup=await inline_keyboards(
            **data,
            create_category=answers.create_category
        )
    )
