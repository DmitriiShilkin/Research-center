from pydantic import BaseModel


class SettingsInfo(BaseModel):
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int
