from tortoise import Tortoise

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


# Инициализация подключения к базе данных
async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": MODELS}  # путь до моделей
    )


# Закрытие подключения при завершении работы приложения
async def close_db():
    await Tortoise.close_connections()
