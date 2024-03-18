from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_keyboards_generator(row: int = 1, **kvargs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for key, value in kvargs.items():
        builder.add(InlineKeyboardButton(
            text=f"{value}",
            callback_data=f"{key}"),
        )

    builder.adjust(row)
    keyboard = builder.as_markup()
    return keyboard
