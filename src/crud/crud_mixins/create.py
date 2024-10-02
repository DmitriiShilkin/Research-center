from typing import Generic

from constants.crud_types import CreateSchemaType, ModelType


class CreateAsync(Generic[CreateSchemaType, ModelType]):
    async def create(
        self,
        *,
        create_schema: CreateSchemaType,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True, mode="json")
        obj = await self.model.create(**data)

        return obj
