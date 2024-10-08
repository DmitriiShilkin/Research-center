from typing import TypedDict

USER_EMAIL = "lakritsa@gmail.com"


class MarketNameContext(TypedDict):
    market_name: str


class TotalAmountContext(TypedDict):
    total_amount: str


class DifferenceContext(TypedDict):
    difference: str


class RateAlertContext(
    MarketNameContext,
    TotalAmountContext,
    DifferenceContext
):
    pass
