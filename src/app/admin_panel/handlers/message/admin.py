from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from src.app.category.services.category import category_service
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.keyboards.default.keyboard_generator import keyboards_generator
from src.core.filters.is_admin import IsAdmin
from src.app.product.states.add_product import AddProductState
from src.app.product.handlers.utils.product import change_product_from_data
from src.app.product import answers

router = Router()


@router.message(IsAdmin(), F.text == 'Команди адміністратора')
async def admin_panel(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(
        'Команди адміністратора',
        reply_markup=await inline_keyboards(
            row=2,
            add_product='Додати товар',
            add_category='Додати категорію',
            zero_quantity='Вивести товар якого не має на складі',
        )
    )
