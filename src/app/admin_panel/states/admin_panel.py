from aiogram.fsm.state import StatesGroup, State


class AdminPanel(StatesGroup):
    add_product = State()
    add_category = State()
    remove_product = State()
    chose_product = State()
    remove_category = State()
    chose_category = State()
    change_product = State()
    change_category = State()
    zero_quantity = State()


class OrderSend(StatesGroup):
    user_message = State()
