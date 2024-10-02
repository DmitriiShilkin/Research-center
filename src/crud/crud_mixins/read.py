from typing import Generic, Optional, Sequence

from constants.crud_types import ModelType


class ReadAsync(Generic[ModelType]):
    async def get_by_id(
        self,
        obj_id: int,
    ) -> Optional[ModelType]:
        return await self.model.filter(id=obj_id).first()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        return await self.model.all().offset(skip).limit(limit)
