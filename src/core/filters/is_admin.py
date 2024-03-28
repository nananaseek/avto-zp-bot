from aiogram.filters import Filter
from aiogram.types import Message

from src.core.services.user import admin_service
from src.settings.config import settings


class IsAdmin(Filter):
    DEBUG = settings.DEBUG

    async def __call__(self, message: Message) -> bool:
        if self.DEBUG:
            return True
        else:
            admin = await admin_service.get(user_id=message.from_user.id)
            return False if admin is None else True
