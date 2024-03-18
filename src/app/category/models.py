import uuid
from uuid import UUID

from tortoise import fields, models

from src.app.product.models import Product


class Category(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=32)
    products: fields.ManyToManyRelation["Product"] = fields.ManyToManyField(
        'models.Product',
        related_name='product_categories'
    )

