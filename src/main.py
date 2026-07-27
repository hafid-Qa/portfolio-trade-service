from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from settings import settings
from api.routes import user_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        yield
    finally:
        pass


app = FastAPI(
    title=settings.API_NAME,
    docs_url=None if settings.PROD else "/docs",
    redoc_url=None if settings.PROD else "/redoc",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"message": f"{settings.API_NAME} working"}

app.include_router(user_router)
