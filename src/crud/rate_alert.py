from crud.crud_mixins import BaseCRUD, CreateAsync, ReadAsync
from models.rate_alert import RateAlert
from schemas.rate_alert import RateAlertCreate


class CRUDRateAlert(
    BaseCRUD[RateAlert],
    CreateAsync[RateAlert, RateAlertCreate],
    ReadAsync[RateAlert],
):
    ...


crud_rate_alert = CRUDRateAlert(RateAlert)
