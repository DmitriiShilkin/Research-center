from tortoise import fields
from tortoise.models import Model


class InitialRate(Model):
    """
    Модель первоначальных значений валютных пар

    ## Attrs
        - id: int - идентификатор
        - name: str - название пары
        - value: str - значение пары
    """
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=7)
    value = fields.FloatField()

    def __str__(self) -> str:
        return self.name
