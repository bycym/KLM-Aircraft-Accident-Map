from safety_backend.settings import Settings
from fastapi.testclient import TestClient

# from fastapi.testclient import *

from safety_backend.app import create_app

from safety_backend.cache import YEARS_KEY, AccidentCache

from safety_backend.rpc import RpcRequest


class FakeRedis:
    def __init__(self) -> None:
        self.values = {}
        self.sets = []

    def get(self, key: str):
        return self.values.get(key)

    def setex(self, key: str, ttl: int, value: str) -> None:
        self.values[key] = value
        self.sets.append((key, ttl, value))


class FakeRpc:
    def __init__(self, replies=None, raises=None) -> None:
        self.replies = replies or {}
        self.raises = raises

        self.calls: list[RpcRequest] = []

    def call(self, request: RpcRequest):
        self.calls.append(request)

        if self.raises:
            raise self.raises
        return self.replies[request.action]


def test_backend_uses_redis_hit_before_rabbitmq() -> None:
    year = 2019
    redis = FakeRedis()

    cache = AccidentCache(redis, 604800)

    cache.set_json(YEARS_KEY, {"years": [year]})

    rpc = FakeRpc()
    app = create_app(settings=Settings(), cache_factory=lambda _settings: cache, rpc_client=rpc)

    response = TestClient(app).get("/years")

    assert response.status_code == 200
    assert response.json() == {"years": [year]}
    assert rpc.calls == []


def test_out_of_range_year_returns_client_error() -> None:
    rpc = FakeRpc(replies={"years": {"years": [1948, 2019]}})
    app = create_app(
        settings=Settings(),
        cache_factory=lambda _settings: AccidentCache(FakeRedis(), 604800),
        rpc_client=rpc,
    )

    response = TestClient(app).get("/accidents?year=2020")

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "year_out_of_range"
