import uuid
from uuid import UUID

from tortoise import Model, fields, models


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
