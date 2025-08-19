from __future__ import annotations

import asyncio
import time
from typing import Any, Optional

try:
    import aioredis  # type: ignore
except Exception:  # pragma: no cover - optional
    aioredis = None

from .config import get_settings


class Cache:
    def __init__(self) -> None:
        settings = get_settings()
        self.redis_url = settings.redis_url
        self._local: dict[str, tuple[Any, float]] = {}
        self._redis = None
        if self.redis_url and aioredis is not None:
            try:
                self._redis = aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
            except Exception:
                self._redis = None

    async def get(self, key: str) -> Optional[Any]:
        if self._redis is not None:
            return await self._redis.get(key)
        data = self._local.get(key)
        if not data:
            return None
        value, expires = data
        if expires < time.time():
            del self._local[key]
            return None
        return value

    async def set(self, key: str, value: Any, ttl: int) -> None:
        if self._redis is not None:
            await self._redis.set(key, value, ex=ttl)
            return
        self._local[key] = (value, time.time() + ttl)


cache = Cache()
