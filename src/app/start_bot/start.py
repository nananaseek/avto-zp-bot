from aiogram import Router, types
from aiogram.filters import CommandStart

from src.core.keyboards.default.keyboard_generator import keyboards_generator, start_keyboard
from src.core.filters.is_admin import IsAdmin

router = Router()


@router.message(CommandStart())
async def start_bot(message: types.Message):
    admin = IsAdmin()
    await message.answer(
        f'Вітаю в магазині запчастин {message.from_user.username}',
        reply_markup=start_keyboard(is_admin=await admin(message))
    )

