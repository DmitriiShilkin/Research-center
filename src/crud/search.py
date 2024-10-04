from typing import List

from models import RateAlert
from configs.db import close_db, init_db


class CRUDSearch:
    async def get_multi_rate_alert_by_title(
        self,
        query: str,
        skip,
        limit,
    ) -> dict:
        result = dict()
        result["rate_alerts"] = await self._get_rate_alert_result(
            query=query,
            skip=skip,
            limit=limit
        )
        return result

    @staticmethod
    async def _get_rate_alert_result(
        query: str,
        skip: int,
        limit: int,
    ) -> List[RateAlert]:
        await init_db()
        query_filter = " OR ".join([f"key_json->>'title' ILIKE '%{q}%'" for q in query.split()])
        query = f"SELECT * FROM ratealert WHERE {query_filter} ORDER BY id LIMIT {limit} OFFSET {skip}"
        result = await RateAlert.raw(query)
        await close_db()

        return result


crud_search = CRUDSearch()
