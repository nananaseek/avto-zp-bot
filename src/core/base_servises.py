from typing import TypeVar

from pydantic import BaseModel
from tortoise import models
from tortoise.expressions import Q

ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)


class BaseServices:
    model = ModelType
    create_schema = CreateSchemaType
    get_schema = GetSchemaType

    async def create(self, schema: create_schema, **kwargs) -> ModelType:
        return await self.model.create(**schema.model_dump(exclude_unset=True), **kwargs)

    async def get(self, **kwargs) -> ModelType:
        return await self.model.get_or_none(Q(
            **kwargs,
            join_type='OR'
        ))

    async def delete(self, **kwargs) -> None:
        return await self.model.delete(**kwargs)

    async def all(self) -> list[ModelType]:
        all_objects = self.model.all()
        return await self.get_schema.from_queryset(all_objects)

    async def filter(self, obj: bool = False, **kwargs) -> list[ModelType]:
        objects = self.model.filter(Q(
            **kwargs,
            join_type='OR'
        ))
        return objects if obj else await self.get_schema.from_queryset(objects)
