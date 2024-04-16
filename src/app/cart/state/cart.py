from aiogram.fsm.state import StatesGroup, State


class ChooseState(StatesGroup):
    amount = State()
    card_amount = State()


class BuyProduct(StatesGroup):
    buy = State()
    check_address = State()
    check_contact = State()