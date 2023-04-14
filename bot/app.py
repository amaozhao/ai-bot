from typing import Callable

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from .chat.middlewares import TimerHeaderMiddleware
from .chat.models.base import Base
from .chat.routers import auth
from .chat.settings import settings
from .cores.db import async_engine


def start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return start_app


def application():
    _app = FastAPI(debug=settings.DEBUG, title=settings.TITLE, version=settings.VERSION)

    _app.add_event_handler("startup", start_app_handler(_app))
    _app.add_middleware(GZipMiddleware, minimum_size=1000)
    _app.add_middleware(TimerHeaderMiddleware)

    _app.include_router(auth.router)
    return _app


app = application()


@app.get("/")
async def root():
    return {"message": "Hello World"}
