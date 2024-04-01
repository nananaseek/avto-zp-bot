import logging

from aiogram import types
from aiogram.types import InputMediaPhoto

from src.main import bot


async def edit_photo(image: str, text: str, chat_id: int, message_id: int, keyboard=None):
    photo = InputMediaPhoto(
        media=image,
        caption=text
    )
    await bot.edit_message_media(photo, chat_id, message_id=message_id, reply_markup=keyboard)


async def edit_text(text, keyboard, chat_id: int, message_id: int):
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)