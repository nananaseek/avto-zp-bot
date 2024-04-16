from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_queryset
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.utils.dell_message import dell_two_message


router = Router()


@router.message(IsAdmin(), ChangeProductStates.name, F.text)
async def change_name_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].name = message.text
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)


@router.message(IsAdmin(), ChangeProductStates.description, F.text)
async def change_description_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].description = message.text
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)


@router.message(IsAdmin(), ChangeProductStates.image, F.photo)
async def change_image_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].image = message.photo[-1].file_id
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)


@router.message(IsAdmin(), ChangeProductStates.image)
async def image_product(message: types.Message):
    await message.answer(answers.error_get_image)


@router.message(IsAdmin(), ChangeProductStates.price, F.text)
async def change_price_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].price = message.text
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)


@router.message(IsAdmin(), ChangeProductStates.quantity, F.text)
async def change_quantity_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].quantity = message.text
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)


@router.message(IsAdmin(), ChangeProductStates.discount, F.text)
async def change_discount_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['product'].discount = message.text
    await data['product'].save()
    await dell_two_message(chat_id=message.chat.id, message_id=message.message_id)
    await change_product_from_queryset(message, state)
