import uuid

from tortoise import fields, models


class Category(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=32)


