import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.routes import user_router
from domain.exceptions import UnknownStocksInPortfolio
from repositories import InMemoryStockRepository, InMemoryUserPortfolioRepository
from settings import Settings, get_settings


logger = logging.getLogger(__name__)


LifespanType = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def make_lifespan(settings: Settings) -> LifespanType:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        app.state.stock_repo = InMemoryStockRepository.from_yaml(settings.stock_path)
        app.state.portfolio_repo = InMemoryUserPortfolioRepository.from_yaml(
            settings.portfolio_path
        )
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

    @app.exception_handler(UnknownStocksInPortfolio)
    async def handle_unknown_stocks(
        request: Request, exc: UnknownStocksInPortfolio
    ) -> JSONResponse:
        logger.exception("portfolio references unknown stocks", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "internal error"}
        )

    return app


app = create_app(get_settings())
