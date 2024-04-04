from aiogram.fsm.state import StatesGroup, State


class CartState(StatesGroup):
    check = State()
    dell_product = State()
    add_product = State()

