import json
from typing import Any


YEARS_KEY = "accident_years"


class AccidentCache:
    def __init__(self, redis_client: Any, ttl_seconds: int) -> None:
        self.redis = redis_client

        self.ttl_seconds = ttl_seconds

    @staticmethod
    def accidents_key(year: int) -> str:
        return f"accidents:{year}"

    def get_json(self, key: str) -> Any | None:
        value = self.redis.get(key)

        if value is None:
            return None
        if isinstance(value, bytes):
            # database has latin-1 values, make sure everything is fine
            value = value.decode("utf-8")
        return json.loads(value)

    def set_json(self, key: str, value: Any) -> None:
        self.redis.setex(key, self.ttl_seconds, json.dumps(value))
