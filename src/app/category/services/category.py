import logging

from src.app.category.schemas.category import Pydantic_Category_Create, Pydantic_Category_Get
from src.core.base_servises import BaseServices
from src.app.category.models import Category


class CategoryService(BaseServices):
    model = Category
    create_schema = Pydantic_Category_Create
    get_schema = Pydantic_Category_Get

    async def add_product_to_category(self, category_id: str, product):
        category = await self.model.get_or_none(id=category_id)
        if category:
            await category.products.add(product)
        else:
            return None


category_service = CategoryService()
