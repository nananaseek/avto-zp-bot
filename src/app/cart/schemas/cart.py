from typing import List

from pydantic import BaseModel


class CreateItem(BaseModel):
    image: str
    description: str
    name: str
    price: float
    quantity: int
    discount: float


class CreateOrder(BaseModel):
    items: List[CreateItem]




