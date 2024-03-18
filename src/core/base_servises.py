from typing import TypeVar

from pydantic import BaseModel
from tortoise import models


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
        return await self.model.get_or_none(**kwargs)

    async def delete(self, **kwargs) -> None:
        return await self.model.delete(**kwargs)

    async def all(self) -> list[ModelType]:
        all_objects = self.model.all()
        return await self.get_schema.from_queryset(all_objects)
