from tortoise import Tortoise

from src.core.utils.get_models import get_app_list
from src.settings.config import settings


class Database:
    ORM = Tortoise
    DB_URL = settings.DB_URL
    DB_MODELS = {'models': get_app_list()}

    async def startup(self):
        await self.ORM.init(
            db_url=self.DB_URL,
            modules=self.DB_MODELS
        )
        await self.ORM.generate_schemas()

    async def shutdown(self):
        await self.ORM.close_connections()


db = Database()
