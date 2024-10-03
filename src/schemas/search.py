from typing import List
from pydantic import BaseModel

from schemas.rate_alert import RateAlertResponse


class SearchRateAlertResponse(BaseModel):
    rate_alerts: List[RateAlertResponse]
