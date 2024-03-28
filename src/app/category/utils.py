from typing import List, Dict

from aiogram.types import Message

from src.app.category.models import Category
from src.app.category.services.category import category_service
from src.core.keyboards.inline.keyboard_generator import inline_pagination
from src.core.keyboards.inline.keyboard_generator import inline_keyboards_generator as inline_keyboards


class CategoryUtils:
    @staticmethod
    async def get_category_dict() -> dict:
        category_list = await category_service.all()
        return {f'{category.id}': category.name for category in category_list}

    async def get_category_and_inline(self, text: str, message: Message):
        category_dict = await self.get_category_dict()
        await message.answer(
            text=text,
            reply_markup=await inline_pagination(
                row=2,
                size=6,
                **category_dict
            ) if len(category_dict) > 6 else await inline_keyboards(
                row=2,
                **category_dict
            )
        )

        return category_dict


category_utils = CategoryUtils()

