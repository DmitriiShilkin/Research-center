from decimal import Decimal
from typing import Dict

from crud.initial_rate import crud_initial_rate
from schemas.initial_rate import InitialRateCreate, InitialRateUpdate


async def create_initial_rate(create_data: Dict) -> None:
    try:
        schema = InitialRateCreate(
            **create_data,
        )
        await crud_initial_rate.create(
            create_schema=schema
        )
    except ValueError:
        raise


async def update_initial_rate(name: str, value: Decimal) -> None:
    obj = await crud_initial_rate.get_by_name(name)
    try:
        schema = InitialRateUpdate(
            value=value
        )
        await crud_initial_rate.update(
            db_obj=obj,
            update_data=schema
        )
    except ValueError:
        raise
