from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from api.v1.router import router as v1_router
from configs.config import app_settings
from configs.db import DB_URL, MODELS
from constants.backend import BACKEND_ENTRYPOINT


# Инициализация подключения к базе данных
async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": MODELS}  # путь до моделей
    )


# Закрытие подключения при завершении работы приложения
async def close_db():
    await Tortoise.close_connections()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="RC",
    openapi_url=f"/{BACKEND_ENTRYPOINT}/openapi.json/",
    docs_url=f"/{BACKEND_ENTRYPOINT}/docs/",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=f"/{BACKEND_ENTRYPOINT}")


if __name__ == "__main__":
    host = "0.0.0.0"  # noqa: S104
    if app_settings.ENVIRONMENT == "local":
        uvicorn.run(
            "main:app",
            host=host,
            port=app_settings.SERVICE_PORT,
            reload=True,
            forwarded_allow_ips="*",
        )
    else:
        uvicorn.run(
            "main:app",
            host=host,
            port=8000,
            forwarded_allow_ips="*",
            workers=app_settings.UVICORN_WORKERS,
        )
