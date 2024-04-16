import logging

from src.core.database.redis.connect import sessions
from src.settings.config import settings


class SessionServices:
    REDIS = sessions
    USER_EXPIRES = settings.SESSION_EXPIRE_MINUTES
    ADMIN_EXPIRES = settings.ADMIN_SESSION_EXPIRE_MINUTES

    async def create_user_session(self, user_id):
        await self.REDIS.set(user_id, 0, ex=self.USER_EXPIRES)

    async def create_admin_session(self, user_id):
        await self.REDIS.set(user_id, 1, ex=self.ADMIN_EXPIRES)

    async def update_user_session(self, user_id):
        await self.REDIS.expire(user_id, self.USER_EXPIRES)

    async def update_admin_session(self, user_id):
        await self.REDIS.expire(user_id, self.ADMIN_EXPIRES)

    async def get_session(self, user_id) -> bool:
        return bool(int(await self.REDIS.get(user_id)))

    async def get_user_session(self, user_id) -> bool:
        return await self.REDIS.exists(user_id)


session_services = SessionServices()
