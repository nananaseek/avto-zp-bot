from aiogram import types

from src.main import bot


async def dell_two_message(chat_id: int, message_id: int):
    msg_id = (message_id, message_id - 1)
    await bot.delete_messages(chat_id, msg_id)


async def dell_target_message(chat_id: int, message_id: int):
    await bot.delete_message(chat_id, message_id)
