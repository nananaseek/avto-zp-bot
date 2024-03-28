from aiogram import Router
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.keyboards.inline.pagination import Paginator


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


async def inline_pagination(
        row: int = 1,
        state: State = None,
        size: int = 8,
        dp: Router | None = None,
        **kvargs
):
    kb = Paginator(
        data=await inline_keyboards_generator(
            row,
            **kvargs
        ),
        state=state,
        size=size,
        dp=dp
    )
    return kb()
