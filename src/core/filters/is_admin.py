from aiogram.filters import Filter
from aiogram.types import Message

from src.core.services.session_services import session_services
from src.core.services.user import admin_service
from src.settings.config import settings


class IsAdmin(Filter):
    DEBUG = settings.DEBUG

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        # if self.DEBUG:
        #     return True
        # else:
        if not await session_services.get_admin_session(user_id):
            admin = await admin_service.get(obj=True, user_id=user_id)
            if admin is None:
                return False
            else:
                await session_services.create_admin_session(user_id=user_id)
                return True
