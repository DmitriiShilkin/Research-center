from typing import Optional

from configs.db import init_db, close_db
from crud.async_crud import BaseAsyncCRUD
from models.initial_rate import InitialRate
from schemas.initial_rate import InitialRateCreate, InitialRateUpdate


class CRUDInitialRate(
    BaseAsyncCRUD[InitialRate, InitialRateCreate, InitialRateUpdate],
):
    async def get_by_name(self, name: str) -> Optional[InitialRate]:
        await init_db()
        obj = await self.model.filter(name=name).first()
        await close_db()

        return obj


crud_initial_rate = CRUDInitialRate(InitialRate)
