from typing import Generic

from constants.crud_types import CreateSchemaType, ModelType
from configs.db import close_db, init_db


class CreateAsync(Generic[CreateSchemaType, ModelType]):
    async def create(
        self,
        *,
        create_schema: CreateSchemaType,
    ) -> ModelType:
        await init_db()
        data = create_schema.model_dump(exclude_unset=True, mode="json")
        obj = await self.model.create(**data)
        await close_db()

        return obj
