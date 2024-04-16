import uuid
from uuid import UUID

from tortoise import Model, fields, models

from src.app.category.models import Category


class Product(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    image = fields.CharField(max_length=256, null=True)
    description = fields.CharField(max_length=320)
    name = fields.CharField(max_length=128)
    price = fields.DecimalField(max_digits=1000, decimal_places=2)
    # чи є товар на складі
    quantity = fields.IntField()
    discount = fields.DecimalField(max_digits=100, decimal_places=1, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    categories: fields.ManyToManyRelation["Category"] = fields.ManyToManyField(
            'models.Category',
            related_name='product_categories'
        )

    def discount_price(self):
        if self.discount is None:
            new_price = self.price - (self.price * self.discount / 100)
            return f'<s>{self.price}₴</s> {new_price:.2f}₴'
        else:
            return f'{self.price}'

    class PydanticMeta:
        computed = ["discount_price",]
        allow_cycles = True


class Admins(Model):
    user_id = fields.IntField(pk=True)
