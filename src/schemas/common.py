import re

from pydantic import BaseModel, Field, field_validator

from constants.auth import MIN_PASSWORD_LENGTH


class PasswordBase(BaseModel):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def password_validation(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH and not re.match(r"^[ -~]+$", v):
            msg = "Password does not meet the requirements."
            raise ValueError(msg)
        return v
