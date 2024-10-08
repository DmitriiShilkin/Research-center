from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import PositiveInt

from crud.rate_alert import crud_rate_alert
from schemas.rate_alert import (
    RateAlertCreate,
    RateAlertUpdate,
    RateAlertResponse,
)

router = APIRouter()


@router.get("/", response_model=List[RateAlertResponse])
async def read_rate_alerts(
    skip: int = 0,
    limit: int = 100,
):
    return await crud_rate_alert.get_multi(
        skip=skip,
        limit=limit
    )


@router.patch(
    "/{rate_alert_id}/",
    response_model=RateAlertResponse
)
async def update_rate_alert(
    rate_alert_id: PositiveInt,
    update_data: RateAlertUpdate,
):
    found_rate_alert = await crud_rate_alert.get_by_id(
        obj_id=rate_alert_id
    )
    if not found_rate_alert:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Rate alert not found"
        )

    return await crud_rate_alert.update(
        db_obj=found_rate_alert, update_data=update_data
    )


@router.delete(
    "/{rate_alert_id}/",
    response_model=RateAlertResponse
)
async def delete_rate_alert(
    rate_alert_id: PositiveInt,
):
    found_rate_alert = await crud_rate_alert.get_by_id(
        obj_id=rate_alert_id
    )
    if not found_rate_alert:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Rate alert not found"
        )

    return await crud_rate_alert.remove(obj_id=rate_alert_id)
