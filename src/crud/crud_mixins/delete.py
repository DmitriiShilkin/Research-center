from typing import Generic, Optional

from constants.crud_types import ModelType
from configs.db import close_db, init_db


class DeleteAsync(Generic[ModelType]):
    async def remove(
        self,
        *,
        obj_id: int
    ) -> Optional[ModelType]:
        await init_db()
        obj = await self.model.get_or_none(id=obj_id)
        if not obj:
            return None

        await obj.delete()
        await close_db()

        return obj
