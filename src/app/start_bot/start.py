from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from src.app.category.services.category import category_service
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.keyboards.default.keyboard_generator import keyboards_generator
from src.core.filters.is_admin import IsAdmin
from src.app.product.states.add_product import AddProductState
from src.app.product.handlers.utils.product import change_product
from src.app.product import answers

router = Router()


@router.message(CommandStart())
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(
        f'Вітаю в магазині запчастин {message.from_user.username}',
        reply_markup=await keyboards_generator('Наявні товари')
    )