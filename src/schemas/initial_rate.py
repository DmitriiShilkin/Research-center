from typing import Optional
from pydantic import BaseModel

from constants.custom_types import DecimalJsonType


class InitialRateBase(BaseModel):
    name: str
    value: DecimalJsonType


class InitialRateCreate(InitialRateBase):
    ...


class InitialRateUpdate(InitialRateBase):
    name: Optional[str] = None
