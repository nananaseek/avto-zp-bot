from aiogram.fsm.state import StatesGroup, State


class ChangeProductStates(StatesGroup):
    change_product = State()
    delete_product = State()
