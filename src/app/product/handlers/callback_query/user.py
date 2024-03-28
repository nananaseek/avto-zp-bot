from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from src.app.product import answers
from src.app.product.handlers.commands.admin import add_product
from src.app.product.handlers.utils.product import change_product_from_data, save_product, send_product_list
from src.app.product.services.product import product_service
from src.app.product.states.search_product import SearchProduct
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState

router = Router()


@router.callback_query(F.data == 'send_all_products', SearchProduct.search)
async def send_all_products(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    product_list = await product_service.filter(quantity__gt=0)

    await send_product_list(product_list, query.message)
