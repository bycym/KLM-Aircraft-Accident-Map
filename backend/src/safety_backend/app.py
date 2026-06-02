from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis

from .logger import logger

from safety_backend.cache import YEARS_KEY, AccidentCache
from safety_backend.lambda_client import LambdaDatabaseClient
from safety_backend.models import AccidentYearResponse, ErrorResponse, YearsResponse


from safety_backend.rpc import RabbitRpcClient, RpcRequest, RpcTimeoutError
from safety_backend.settings import Settings


def create_app(
    settings: Settings | None = None,
    cache_factory: Any | None = None,
    rpc_client: Any | None = None,
) -> FastAPI:

    app_settings = settings or Settings()

    app = FastAPI(title="Aircraft Accident Map API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:8082"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    cache = cache_factory(app_settings) if cache_factory else _build_cache(app_settings)
    rpc = rpc_client or _build_database_client(app_settings)

    def get_cache() -> AccidentCache:
        return cache

    def get_rpc() -> Any:
        return rpc

    @app.get("/health")
    def health():
        logger.info("Health")
        return {"status": "ok"}

    @app.get("/years", response_model=YearsResponse, responses={503: {"model": ErrorResponse}})
    def years(
        accident_cache: AccidentCache = Depends(get_cache), accident_rpc: Any = Depends(get_rpc)
    ) -> dict[str, Any]:
        logger.info("Get Years")

        cached = accident_cache.get_json(YEARS_KEY)
        if cached is not None:
            return cached

        try:
            payload = accident_rpc.call(RpcRequest(action="years", payload={}))
        except RpcTimeoutError as exc:
            raise HTTPException(
                status_code=503,
                detail={"error": "database timoeut", "detail": str(exc)},
            ) from exc
        accident_cache.set_json(YEARS_KEY, payload)
        return payload

    @app.get(
        "/accidents",
        response_model=AccidentYearResponse,
        responses={400: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    )
    def accidents(
        year: int = Query(..., ge=1000, le=9999),
        accident_cache: AccidentCache = Depends(get_cache),
        accident_rpc: Any = Depends(get_rpc),
    ) -> dict[str, Any]:
        logger.info("Get accidents")
        cached = accident_cache.get_json(AccidentCache.accidents_key(year))
        if cached is not None:
            return cached

        available_years = years(accident_cache, accident_rpc)["years"]
        if available_years and (year < min(available_years) or year > max(available_years)):
            raise HTTPException(
                status_code=400,
                detail={"error": "year_out_of_range", "detail": "year is outside dataset range"},
            )
        try:
            payload = accident_rpc.call(RpcRequest(action="accidents_by_year", payload={"year": year}))

        except RpcTimeoutError as exc:
            raise HTTPException(
                status_code=503,
                detail={"error": "database_timeout", "detail": str(exc)},
            ) from exc

        accident_cache.set_json(AccidentCache.accidents_key(year), payload)
        return payload

    return app


def _build_cache(settings: Settings) -> AccidentCache:
    logger.info("build cache")
    return AccidentCache(Redis.from_url(settings.redis), settings.cache_ttl_seconds)


def _build_database_client(settings: Settings) -> Any:
    logger.info("_build_database_client")
    if settings.database_client == "lambda":
        return LambdaDatabaseClient(settings.database_lambda_function_name)
    return RabbitRpcClient(settings.rabbitmq_url, settings.rpc_queue, settings.rpc_timeout_seconds)
