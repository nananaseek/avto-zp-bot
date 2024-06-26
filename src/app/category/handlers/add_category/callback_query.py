import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.app.category.schemas.category import Pydantic_Category_Create
from src.app.category.services.category import category_service
from src.app.category.states.create_category import CreateCategory
from src.app.category import answers

callback_router = Router()


@callback_router.callback_query(F.data == 'name', CreateCategory.is_correct)
async def rename_category(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateCategory.name)
    await query.message.answer(answers.enter_category_name)


@callback_router.callback_query(F.data == 'create_category', CreateCategory.is_correct)
async def create_category(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        category_schema = Pydantic_Category_Create(name=data['name'])
        await category_service.create(category_schema)
    except Exception as e:
        logging.error(f'Error with create category: {e}')

    await query.message.answer(answers.category_is_created)

