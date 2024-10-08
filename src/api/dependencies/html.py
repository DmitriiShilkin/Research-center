from typing import AsyncGenerator, Generator

from jinja2 import Environment, FileSystemLoader, select_autoescape

from configs.config import app_settings

if app_settings.ENVIRONMENT in ("development", "production"):
    main_path = "/app/src/templates"
else:
    main_path = "src/templates"

paths = ["/src/templates", "templates", main_path]


async def get_async_env() -> AsyncGenerator[Environment, None]:
    env = Environment(
        loader=FileSystemLoader(paths),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=True,
    )
    yield env


def get_sync_env() -> Generator[Environment, None, None]:
    env = Environment(
        loader=FileSystemLoader(paths),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=False,
    )
    yield env
