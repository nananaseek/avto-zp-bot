from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def keyboards_generator(*args) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=value) for value in args
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="test"
    )

    return keyboard
