from typing import Generic, Optional

from constants.crud_types import ModelType


class DeleteAsync(Generic[ModelType]):
    async def remove(
        self,
        *,
        obj_id: int
    ) -> Optional[ModelType]:
        obj = await self.model.get_or_none(id=obj_id)
        if not obj:
            return None

        await obj.delete()
        return obj
