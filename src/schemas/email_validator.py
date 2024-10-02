from pydantic import EmailStr
from pydantic.networks import validate_email


class EmailStrLower(EmailStr):
    @classmethod
    def _validate(
        cls, __input_value: str, /
    ) -> str:
        return validate_email(__input_value)[1].lower()
