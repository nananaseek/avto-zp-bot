from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.product.models import Product


Pydantic_Product_Get = pydantic_model_creator(Product, name="Pydantic_Product_Get", exclude_readonly=True)
Pydantic_Product_Create = pydantic_model_creator(
    Product,
    name="create_product",
    exclude=(
        'id',
        'cart',
        'created_at',
        'updated_at'
    )
)
