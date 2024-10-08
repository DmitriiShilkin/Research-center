from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Annotated
from pydantic import BaseModel, Field, PositiveInt, PlainSerializer

from constants.rate_alert import COINS


class MinMax(BaseModel):
    min_price: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]
    max_price: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]


class KashItem(BaseModel):
    price: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]
    minmax: List[MinMax]


class KeyJson(BaseModel):
    title: str
    kash: List[KashItem]
    difference: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]
    total_amount: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]
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
