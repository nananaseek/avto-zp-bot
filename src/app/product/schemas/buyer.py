from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.product.models import Buyer


Pydantic_Buyer_Get = pydantic_model_creator(Buyer, name="Pydantic_Buyer_Get")
