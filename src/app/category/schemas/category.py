from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.category.models import Category


Pydantic_Category_Get = pydantic_model_creator(Category, name="category")
Pydantic_Category_Create = pydantic_model_creator(
    Category,
    name="Pydantic_Product_Create",
    exclude=('id',)
)
