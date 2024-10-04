from typing import Generic, Union

from pydantic import BaseModel

from constants.crud_types import ModelType, UpdateSchemaType
from configs.db import close_db, init_db


class UpdateAsync(Generic[ModelType, UpdateSchemaType]):
    async def update(
        self,
        *,
        db_obj: ModelType,
        update_data: Union[UpdateSchemaType, dict],
    ) -> ModelType:
        await init_db()
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True, mode="json")
        await self.model.filter(id=db_obj.id).update(**update_data)

        obj = await self.model.get(id=db_obj.id)
        await close_db()

        return obj
