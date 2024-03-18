from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.app.category.services.category import category_service
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.core.filters.is_admin import IsAdmin
from src.app.product.states.add_product import AddProductState
from src.app.product.handlers.utils.product import change_product
from src.app.product import answers

router = Router()


@router.message(IsAdmin(), F.text, AddProductState.name)
async def name_product(message: types.Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    if data['is_correct']:
        await state.set_state(AddProductState.description)
        await message.answer(answers.enter_description_product)
    else:
        await change_product(data, message, state)


@router.message(IsAdmin(), F.text, AddProductState.description)
async def description_product(message: types.Message, state: FSMContext):
    data = await state.update_data(description=message.text)
    if data['is_correct']:
        await state.set_state(AddProductState.image)
        await message.answer(answers.enter_image_product)
    else:
        await change_product(data, message, state)


@router.message(IsAdmin(), F.photo, AddProductState.image)
async def image_product(message: types.Message, state: FSMContext):
    data = await state.update_data(image=message.photo[-1].file_id)
    if data['is_correct']:
        await state.set_state(AddProductState.quantity)
        await message.answer(answers.enter_quantity_product)
    else:
        await change_product(data, message, state)


@router.message(IsAdmin(), AddProductState.image)
async def image_product(message: types.Message):
    await message.answer(answers.error_get_image)


@router.message(IsAdmin(), F.text, AddProductState.quantity)
async def quantity_product(message: types.Message, state: FSMContext):
    data = await state.update_data(quantity=message.text)
    if data['is_correct']:
        await state.set_state(AddProductState.price)
        await message.answer(answers.enter_price_product)
    else:
        await change_product(data, message, state)


@router.message(IsAdmin(), F.text, AddProductState.price)
async def price_product(message: types.Message, state: FSMContext):
    data = await state.update_data(price=message.text)
    if data['is_correct']:
        await state.set_state(AddProductState.is_discount)
        await message.answer(
            answers.is_discount_message,
            reply_markup=await inline_keyboards(yes='Так', no='Ні')
        )
    else:
        await change_product(data, message, state)


@router.message(IsAdmin(), F.text, AddProductState.discount)
async def discount_product(message: types.Message, state: FSMContext):
    data = await state.update_data(discount=message.text, is_correct=False)
    await change_product(data, message, state)
