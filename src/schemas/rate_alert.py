from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel, Field, PositiveInt

from constants.custom_types import DecimalJsonType
from constants.rate_alert import COINS


class MinMax(BaseModel):
    min_price: DecimalJsonType
    max_price: DecimalJsonType


class KashItem(BaseModel):
    price: DecimalJsonType
    minmax: List[MinMax]


class KeyJson(BaseModel):
    title: str
    kash: List[KashItem]
    difference: DecimalJsonType
    total_amount: DecimalJsonType
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
