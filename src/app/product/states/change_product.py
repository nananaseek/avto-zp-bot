from aiogram.fsm.state import StatesGroup, State


class ChangeProductStates(StatesGroup):
    change_product = State()
    delete_product = State()
    is_category = State()
    category = State()
    name = State()
    description = State()
    image = State()
    price = State()
    quantity = State()
    is_discount = State()
    discount = State()
    save_product = State()
    change_product_data = State()