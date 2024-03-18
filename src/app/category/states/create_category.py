from aiogram.fsm.state import StatesGroup, State


class CreateCategory(StatesGroup):
    name = State()