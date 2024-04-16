from src.main import bot


async def send_message_to_user(chat_id: int, text: str, keyboard=None):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=None if keyboard is None else keyboard
    )
