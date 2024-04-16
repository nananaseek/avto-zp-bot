from typing import List

from src.app.product.schemas.product import Pydantic_Product_Create, Pydantic_Product_Get
from src.core.services.base_servises import BaseServices
from src.app.product.models import Product


class ProductService(BaseServices):
    model = Product
    create_schema = Pydantic_Product_Create
    get_schema = Pydantic_Product_Get

    async def get_category(self, category_id: str, in_storage: bool = False) -> List[Product]:
        product_list = await self.model.filter(
            categories__id=category_id,
            **{'quantity__gt': 0} if in_storage else None
        )
        return await self.serialize_product(product_list)

    async def serialize_product(self, product_list: List[Product]):
        serialized = []
        if len(product_list) > 0:
            for product in product_list:
                serialized.append(await self.get_schema.from_tortoise_orm(product))
        return serialized

    async def buy_product(self, product_id: str, quantity_to_buy: int):
        product = await self.model.get_or_none(id=product_id)
        if product is None:
            return True
        else:
            if int(product.quantity) < quantity_to_buy or int(product.quantity) == 0:
                return False
            else:
                product.quantity = int(product.quantity) - quantity_to_buy
                await product.save()
                return True


product_service = ProductService()
