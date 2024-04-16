from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def keyboards_generator(kb_name: str, row: int = 1, *args) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for value in args:
        builder.add(KeyboardButton(text=str(value)))
    builder.adjust(row)
    keyboard = builder.as_markup()

    return keyboard


def contact_keyboard():
    kb = [
        [KeyboardButton(text='Відправити контактну інформацію', request_contact=True)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Натисніть на кнопку щоб надіслати ваші контакти'
    )
    return keyboard


def start_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='Наявні товари'),
            KeyboardButton(text='Товар за категоріями')
        ],
        [KeyboardButton(text='Корзина')],
        [KeyboardButton(text='Команди адміністратора')] if is_admin else []
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Виберіть дію'
    )
    return keyboard
