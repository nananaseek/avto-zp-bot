from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.filters.is_admin import IsAdmin

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

sub_message_router = Router()


@sub_message_router.message(IsAdmin(), CreateCategory.name)
async def add_name(message: types.Message, state: FSMContext):
    await state.set_state(CreateCategory.is_correct)
    data = await state.update_data(name=message.text)

    await message.answer(
        answers.edit_category,
        reply_markup=await inline_keyboards(
            **data,
            create_category=answers.create_category
        )
    )
