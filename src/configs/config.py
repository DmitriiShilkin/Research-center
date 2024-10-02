from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class AppSettings(BaseSetting):
    BASE_DIR: Path = BASE_DIR
    SERVICE_NAME: str
    SERVICE_VERSION: str
    API_VERSION: str
    ENVIRONMENT: str
    DEBUG: bool
    SERVICE_PORT: int
    EXTERNAL_SERVICE_SCHEMA: str = "http"
    EXTERNAL_SERVICE_HOST: str
    EXTERNAL_SERVICE_PORT: int
    SENTRY_DSN: str = ""
    APP_RELEASE: str = ""
    UVICORN_WORKERS: int = 1

    @property
    def full_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}:"
            f"{self.EXTERNAL_SERVICE_PORT}"
        )

    @property
    def full_url_without_port(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}"
        )


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int  # minutes
    JWT_REFRESH_TOKEN_EXPIRES: int  # minutes


class PasswordSettings(BaseSetting):
    PASSWORD_SCORE_MIN: int = 1


class CryptoAPISettings(BaseSetting):
    X_CMC_PRO_API_KEY: str


app_settings = AppSettings()
db_settings = DBSettings()
jwt_settings = JWTSettings()
crypto_api_settings = CryptoAPISettings()
