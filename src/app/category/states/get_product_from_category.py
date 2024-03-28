from aiogram.fsm.state import StatesGroup, State


class GetProductFromCategory(StatesGroup):
    get_product = State()
