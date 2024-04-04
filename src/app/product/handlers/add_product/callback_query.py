import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.admin_panel.states.admin_panel import AdminPanel
from src.app.category.services.category import category_service
from src.app.category.utils import category_utils
from src.app.product import answers
from src.app.product.handlers.utils.product import change_product_from_data, save_product
from src.app.product.services.product import product_service
from src.app.product.states.change_product import ChangeProductStates
from src.core.filters.is_admin import IsAdmin
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards
from src.app.product.states.add_product import AddProductState
from .command import add_product

router = Router()


@router.callback_query(F.data == 'yes', AddProductState.is_discount)
async def yes_discount(query: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(discount=query.message.text, is_correct=False)
    await query.message.answer(answers.yes_discount_message)
    await state.set_state(AddProductState.discount)


@router.callback_query(F.data == 'no', AddProductState.is_discount)
async def no_discounted(query: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(discount=None, is_correct=False)
    await change_product_from_data(data, query.message, state)


@router.callback_query(F.data == 'category', AddProductState.save_product)
async def rename_product(query: types.CallbackQuery, state: FSMContext):
    await category_utils.get_category_and_inline(answers.enter_category_name, query.message)
    await state.set_state(AddProductState.is_category)


@router.callback_query(F.data == 'name', AddProductState.save_product)
async def rename_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_product_name)
    await state.set_state(AddProductState.name)


@router.callback_query(F.data == 'description', AddProductState.save_product)
async def change_description_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_description_product)
    await state.set_state(AddProductState.description)


@router.callback_query(F.data == 'image', AddProductState.save_product)
async def is_change_image_product(query: types.CallbackQuery, state: FSMContext):
    photo = await state.get_data()
    await query.message.answer_photo(
        photo['image'],
        reply_markup=await inline_keyboards(change_photo='Змінити?')
    )


@router.callback_query(F.data == 'change_photo', AddProductState.save_product)
async def is_change_image_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_image_product)
    await state.set_state(AddProductState.image)


@router.callback_query(F.data == 'quantity', AddProductState.save_product)
async def change_quantity_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_quantity_product)
    await state.set_state(AddProductState.quantity)


@router.callback_query(F.data == 'price', AddProductState.save_product)
async def change_price_product(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_price_product)
    await state.set_state(AddProductState.price)


@router.callback_query(F.data == 'discount', AddProductState.save_product)
async def change_discount(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.yes_discount_message)
    await state.set_state(AddProductState.discount)


@router.callback_query(F.data == 'create_product', AddProductState.save_product)
async def save_category(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await save_product(data, query.message, state)


@router.callback_query(AddProductState.is_category)
async def is_category(query: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(category=query.data)
    if data['is_correct']:
        await query.message.answer(
            f"{answers.category_is_selected}: {data['category_dict'][f'{query.data}']}",
            reply_markup=await inline_keyboards(
                row=2,
                yes='Так',
                no='Ні'
            )
        )
        await state.set_state(AddProductState.category)
    else:
        await change_product_from_data(data, query.message, state)


@router.callback_query(F.data == 'yes', AddProductState.category)
async def is_category(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(answers.category_selected)
    await query.message.answer(answers.enter_product_name)
    await state.set_state(AddProductState.name)


@router.callback_query(F.data == 'no', AddProductState.category)
async def is_category(query: types.CallbackQuery, state: FSMContext):
    await add_product(query.message, state)


@router.callback_query(IsAdmin(), F.data == 'add_product')
async def command_add_product(query: types.CallbackQuery, state: FSMContext):
    await add_product(query.message, state)

