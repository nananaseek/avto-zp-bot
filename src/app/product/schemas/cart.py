from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.product.models import Cart


Pydantic_Buyer_Get = pydantic_model_creator(Cart, name="Pydantic_Cart_Get")
