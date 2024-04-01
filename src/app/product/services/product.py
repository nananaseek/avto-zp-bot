from src.app.product.schemas.product import Pydantic_Product_Create, Pydantic_Product_Get
from src.core.base_servises import BaseServices
from src.app.product.models import Product


class ProductService(BaseServices):
    model = Product
    create_schema = Pydantic_Product_Create
    get_schema = Pydantic_Product_Get

    async def get_category(self):
        product = await self.model.get(name='fdsa')
        return await product.categories.all()


product_service = ProductService()
