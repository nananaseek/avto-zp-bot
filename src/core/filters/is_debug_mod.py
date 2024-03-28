from aiogram.filters import Filter
from aiogram.types import Message

from src.settings.config import settings


class IsDebugMode(Filter):
    IS_DEBUG_MODE = settings.DEBUG

    async def __call__(self, message: Message) -> bool:
        return self.IS_DEBUG_MODE
