from contextlib import asynccontextmanager
import schedule
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router as v1_router
from configs.config import app_settings
from constants.backend import BACKEND_ENTRYPOINT

from constants.scheduler import RUN_INTERVAL_MINUTES
from services.rate_alert import perform_scheduled_tasks
from services.scheduler import run_continuously, schedule_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск фоновой задачи для schedule каждый час
    schedule.every(RUN_INTERVAL_MINUTES).minutes.do(schedule_task, perform_scheduled_tasks)
    # запуск фоновой задачи в отдельном потоке
    stop_run_continuously = run_continuously()
    yield
    # остановка фоновой задачи
    stop_run_continuously.set()


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
