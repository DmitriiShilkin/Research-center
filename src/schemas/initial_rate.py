from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, PlainSerializer


class InitialRateBase(BaseModel):
    name: str
    value: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]


class InitialRateCreate(InitialRateBase):
    ...


class InitialRateUpdate(InitialRateBase):
    name: Optional[str] = None
