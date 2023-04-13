from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .chat.settings import settings
from .chat.middlewares import TimerHeaderMiddleware
from .chat.routers import auth


def application():
    _app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        version=settings.VERSION
    )
    _app.add_middleware(GZipMiddleware, minimum_size=1000)
    _app.add_middleware(TimerHeaderMiddleware)

    _app.include_router(auth.router)
    return _app


app = application()


@app.get("/")
async def root():
    return {"message": "Hello World"}
