import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.app.category.schemas.category import Pydantic_Category_Create
from src.app.category.services.category import category_service

from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

sub_callback_router = Router()


@sub_callback_router.callback_query(F.data == 'name', CreateCategory.name)
async def rename_category(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(answers.enter_category_name)


@sub_callback_router.callback_query(F.data == 'create_category', CreateCategory.name)
async def create_category(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        category_schema = Pydantic_Category_Create(name=data['name'])
        await category_service.create(category_schema)
    except Exception as e:
        logging.error(f'Error with create category: {e}')

    await query.message.answer(answers.category_is_created)
