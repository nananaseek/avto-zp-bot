from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.app.category.schemas.category import Pydantic_Category_Get
from src.app.category.services.category import category_service
from src.app.product.schemas.product import Pydantic_Product_Create
from src.app.product.states.add_product import AddProductState
from src.core.filters.is_debug_mod import IsDebugMode
from src.core.filters.is_admin import IsAdmin
from src.core.services.user import admin_service
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards

router = Router()


@router.message(IsDebugMode(), IsAdmin(), Command('info'))
async def user_info(message: types.Message):
    is_admin = await admin_service.get(user_id=message.from_user.id)
    debug_user_info = (f"user_id: {message.from_user.id} \n"
                       f"first_name: {message.from_user.first_name}\n"
                       f"last_name: {message.from_user.last_name}\n"
                       f"username: {message.from_user.username}\n"
                       f"is_admin: {'False' if is_admin is None else 'True'}\n"
                       f"is_premium: {message.from_user.is_premium}\n")
    await message.answer(debug_user_info)


@router.message(IsDebugMode(), IsAdmin(), Command('test_keyboard'))
async def test_keyboard(message: types.Message):
    await message.answer(
        'Тестування інлайн клавіатури',
        reply_markup=await inline_keyboards(row=2, yes='Так', no='Ні', mayb='Я не знаю')
    )


@router.message(IsDebugMode(), IsAdmin(), F.data == 'yes')
async def test_keyboard(message: types.Message):
    await message.answer(
        'Ви натиснули так'
    )


@router.message(IsDebugMode(), IsAdmin(), F.data == 'no')
async def test_keyboard(message: types.Message):
    await message.answer(
        'Ви натиснули ні'
    )


async def get_hello_world(message: types.Message):
    await message.answer('Hello World!')


async def get_username(message: types.Message, username: str):
    await message.answer(f'Hello {username}!')


@router.message(IsDebugMode(), IsAdmin(), Command('call'))
async def call(message: types.Message):
    await get_hello_world(message)


@router.message(IsDebugMode(), IsAdmin(), F.photo, Command('test_photo'))
async def test_photo(message: types):
    await message.answer(f'{message.photo[-1].file_id}')


@router.message(IsDebugMode(), IsAdmin(), Command('state_info_test'), AddProductState.name)
async def test_state_info(message: types.Message, state: FSMContext):
    st = await state.get_state()
    await message.answer(f'{st}')


@router.message(IsDebugMode(), IsAdmin(), Command('test_product_schema'))
async def test_product_schema(message: types.Message, state: FSMContext):
    schema = Pydantic_Product_Create(
        image='test_image',
        description='test_product_description',
        name='test_product_name',
        price='5',
        quantity='2',
        discount='99',
    )
    await message.answer(f'{schema.dict()}')


@router.message(IsDebugMode(), IsAdmin(), Command('test_get_all_category'))
async def test_get_all_category(message: types.Message, state: FSMContext):
    category_list = await category_service.all()
    d = {f'{category.id}': category.name for category in category_list}
    print(d)
    await message.answer(
        f'category list:',
        reply_markup=await inline_keyboards(
            **d
        )
    )


class TestS(StatesGroup):
    test1 = State()
    test2 = State()


@router.message(IsDebugMode(), IsAdmin(), Command('set_stage_test'))
async def set_stage_test(message: types.Message, state: FSMContext):
    s = await state.get_state()
    if s is None:
        await message.answer('not in state')
    else:
        await message.answer(f'stage test: {s}')
