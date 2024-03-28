from aiogram.fsm.state import StatesGroup, State


class SearchProduct(StatesGroup):
    search = State()