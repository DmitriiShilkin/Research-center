from crud.async_crud import BaseAsyncCRUD
from models.rate_alert import RateAlert
from schemas.rate_alert import RateAlertCreate, RateAlertUpdate


class CRUDRateAlert(
    BaseAsyncCRUD[RateAlert, RateAlertCreate, RateAlertUpdate],
):
    ...


crud_rate_alert = CRUDRateAlert(RateAlert)
