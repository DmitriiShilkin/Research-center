from datetime import datetime, UTC

from tortoise import fields
from tortoise.models import Model


class RateAlert(Model):
    """
    Модель оповещения о повышении курса валюты

    ## Attrs
        - id: int - идентификатор
        - key_json: KeyJson - данные в формате JSON
        - created_at: datetime - дата и время создания
    """
    id = fields.IntField(pk=True, index=True)
    key_json = fields.JSONField()
    created_at = fields.DatetimeField(default=lambda: datetime.now(UTC))

    def __str__(self) -> str:
        return self.key_json.get("title", "No Title")
