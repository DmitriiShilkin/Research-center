from uuid import UUID

from pydantic import BaseModel

from schemas.email_validator import EmailStrLower


class UserLogin(BaseModel):
    email: EmailStrLower
    password: str


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    uid: UUID


class AuthURLResponse(BaseModel):
    url: str
