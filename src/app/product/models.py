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
    cart: fields.ManyToManyRelation["Cart"] = fields.ManyToManyField(
        "models.Cart", related_name="products_cart")
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


class Cart(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    quantity = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Buyer(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.BigIntField()
    cart: fields.OneToOneRelation[Cart] = fields.OneToOneField(
        'models.Cart',
        related_name='buyer_cart',
        on_delete=fields.OnDelete.CASCADE
    )


class Admins(Model):
    user_id = fields.IntField(pk=True)
