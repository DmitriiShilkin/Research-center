from typing import Generic, Union

from pydantic import BaseModel

from constants.crud_types import ModelType, UpdateSchemaType


class UpdateAsync(Generic[ModelType, UpdateSchemaType]):
    async def update(
        self,
        *,
        db_obj: ModelType,
        update_data: Union[UpdateSchemaType, dict],
    ) -> ModelType:
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True, mode="json")
        await self.model.filter(id=db_obj.id).update(**update_data)

        return await self.model.get(id=db_obj.id)
