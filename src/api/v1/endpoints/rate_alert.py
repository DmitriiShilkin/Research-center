from typing import List
from fastapi import APIRouter, HTTPException, status

from crud.rate_alert import crud_rate_alert
from schemas.rate_alert import (
    RateAlertCreate,
    RateAlertResponse,
)
from services.rate_alert import get_final_data

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


@router.post(
    "/",
    response_model=RateAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_rate_alert():

    create_data = await get_final_data()
    try:
        schema = RateAlertCreate(
            **create_data,
        )
        new_rate_alert = await crud_rate_alert.create(
            create_schema=schema
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    return await crud_rate_alert.get_by_id(obj_id=new_rate_alert.id)
