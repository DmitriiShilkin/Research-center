from configs.config import db_settings


# Конфигурация базы данных
DB_URL = (
    f"postgres://{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    f"{db_settings.POSTGRES_HOST}:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)

MODELS = ["models", "aerich.models"]

TORTOISE_ORM = {
    "connections": {
        "default": DB_URL,
    },
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
}
