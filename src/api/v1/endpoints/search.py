from fastapi import APIRouter, Query

from crud.search import crud_search
from schemas.search import SearchRateAlertResponse


router = APIRouter()


@router.get("/rate_alert/", response_model=SearchRateAlertResponse)
async def rate_alert_search(
    query: str = Query(min_length=2),
    skip: int = 0,
    limit: int = 100,
):
    return await crud_search.get_multi_rate_alert_by_title(
        query=query,
        skip=skip,
        limit=limit,
    )
