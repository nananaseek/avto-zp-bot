import logging
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

    async def get(self, obj: bool = False, **kwargs) -> ModelType | GetSchemaType:
        object_from_db = await self.model.get_or_none(Q(
            **kwargs,
            join_type='OR'
        ))
        return object_from_db if obj else await self.get_schema.from_tortoise_orm(object_from_db)

    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            logging.error('Object not found')

    async def all(self) -> list[ModelType]:
        all_objects = self.model.all()
        return await self.get_schema.from_queryset(all_objects)

    async def filter(self, obj: bool = False, **kwargs) -> list[ModelType]:
        objects = self.model.filter(Q(
            **kwargs,
            join_type='OR'
        ))
        return objects if obj else await self.get_schema.from_queryset(objects)

    async def obj_to_schema(self, obj: ModelType = None, objects: list = None) -> GetSchemaType:
        return await self.get_schema.from_tortoise_orm(
            obj
        ) if objects is None else await self.get_schema.from_queryset(objects)
