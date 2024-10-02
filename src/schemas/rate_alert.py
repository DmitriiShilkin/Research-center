from datetime import datetime
from decimal import Decimal
from typing import List, Dict

from pydantic import BaseModel, Field, PositiveInt

from constants.rate_alert import COINS


class MinMax(BaseModel):
    min_price: Decimal
    max_price: Decimal


class KashItem(BaseModel):
    price: Decimal
    minmax: List[MinMax]


class KeyJson(BaseModel):
    title: str
    kash: List[KashItem]
    difference: Decimal
    total_amount: Decimal
    coins: List[Dict[str, str]] = Field(default=COINS)
    date: str


class RateAlertBase(BaseModel):
    key_json: KeyJson


class RateAlertCreate(RateAlertBase):
    ...


class RateAlertUpdate(RateAlertBase):
    ...


class RateAlertResponse(RateAlertBase):
    id: PositiveInt
    created_at: datetime
