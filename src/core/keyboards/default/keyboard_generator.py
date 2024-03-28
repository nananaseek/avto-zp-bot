from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def keyboards_generator(kb_name: str, row: int = 1, *args) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for value in args:
        builder.add(KeyboardButton(text=str(value)))
    builder.adjust(row)
    keyboard = builder.as_markup()

    return keyboard
