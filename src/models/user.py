import uuid
from datetime import datetime, UTC

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    Модель пользователя

    ## Attrs
        - id: int - идентификатор пользователя
        - uid: UUID - уникальный идентификаторпользователя
        - first_name: str - имя пользователя
        - second_name: str - фамилия пользователя
        - username: str - юзернейм пользователя
        - email: str - адрес электронной почты пользователя
        - hashed_password: str - зашифрованный пароль пользователя
        - is_email_verified: bool - признак наличия подтверждения email пользователя
        - is_admin: bool - признак наличия прав администратора
        - is_superuser: bool - признак наличия прав суперпользователя
        - registered_at: datetime - дата и время регистрации пользователя
        - updated_at: datetime - дата и время изменения пользователя
        - last_visited_at: datetime - дата и время последнего визита пользователя
        - last_password_change_at: datetime - дата и время последнего изменения пароля пользователя
    """
    id = fields.IntField(pk=True)
    uid = fields.UUIDField(default=uuid.uuid4, unique=True, index=True)
    first_name = fields.CharField(max_length=50)
    second_name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=50, unique=True, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    hashed_password = fields.CharField(max_length=255, null=True)
    is_email_verified = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    registered_at = fields.DatetimeField(default=lambda: datetime.now(UTC))
    updated_at = fields.DatetimeField(auto_now=True)
    last_visited_at = fields.DatetimeField(null=True)
    last_password_change_at = fields.DatetimeField(null=True)

    @property
    def fullname(self) -> str:
        return f"{self.second_name} {self.first_name}"

    def __str__(self) -> str:
        return f"{self.id} - {self.fullname}"
