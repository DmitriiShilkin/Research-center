from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from email_validator import validate_email
from pydantic import BaseModel
from pydantic.class_validators import validator

from schemas.common import PasswordBase
from schemas.email_validator import EmailStrLower


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: EmailStrLower

    class Config:
        from_attributes = True

    @validator("email")
    def email_check(cls, v: Union[EmailStrLower, str]) -> str:
        email_info = validate_email(v, check_deliverability=True)
        return email_info.normalized


class UserCreate(PasswordBase, UserBase):
    ...


class UserUpdateDB(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    uid: UUID
    username: Optional[str] = None
    last_visited_at: Optional[datetime] = None
