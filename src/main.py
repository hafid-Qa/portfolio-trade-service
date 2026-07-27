from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from api.routes import user_router
from settings import Settings, get_settings


LifespanType = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def make_lifespan(settings: Settings) -> LifespanType:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        pass
        yield

    return lifespan


def create_app(settings: Settings, lifespan: LifespanType | None = None) -> FastAPI:
    app = FastAPI(
        title=settings.API_NAME,
        docs_url=None if settings.PROD else "/docs",
        redoc_url=None if settings.PROD else "/redoc",
        lifespan=lifespan or make_lifespan(settings),
    )

    @app.get("/")
    def read_root():
        return {"message": f"{settings.API_NAME} working"}

    app.include_router(user_router)

    return app


app = create_app(get_settings())
