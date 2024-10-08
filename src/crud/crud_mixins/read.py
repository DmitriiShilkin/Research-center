from typing import Generic, Optional, Sequence

from constants.crud_types import ModelType
from configs.db import close_db, init_db


class ReadAsync(Generic[ModelType]):
    async def get_by_id(
        self,
        obj_id: int,
    ) -> Optional[ModelType]:
        await init_db()
        obj = await self.model.filter(id=obj_id).first()
        await close_db()

        return obj

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        await init_db()
        objs = await self.model.all().offset(skip).limit(limit)
        await close_db()

        return objs
